"""
Motor central da Mission Control AI.

Este modulo combina:
    - Coleta de telemetria (src/telemetria.py)
    - Avaliacao de alertas em codigo Python (src/alertas.py)
    - Construcao dinamica de prompt com dados reais injetados
    - Chamada ao LLM (gpt-oss:120b via Ollama Cloud)

A classe MissionEngine e o ponto de orquestracao - a UI nao precisa
saber nada dos modulos internos, so chama engine.analyze(pergunta)
e recebe texto formatado de volta.
"""

import os
from pathlib import Path
from ollama import Client
from dotenv import load_dotenv

from . import telemetria
from . import alertas


# Carrega variaveis do .env na inicializacao do modulo
load_dotenv()

# Trilha tematica deste projeto (MobilitySat conforme briefing)
TRILHA = "mobilitysat"

# Cliente Ollama configurado uma unica vez no carregamento do modulo
_client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": f"Bearer {os.environ.get('OLLAMA_API_KEY', '')}",
    },
)


def llm(prompt: str, system: str | None = None,
        max_tokens: int = 800, temperature: float = 0.3) -> str:
    """
    Ponto unico de integracao com o LLM (gpt-oss:120b via Ollama Cloud).

    Args:
        prompt: mensagem do usuario (com dados de telemetria embutidos).
        system: system prompt opcional definindo papel da IA.
        max_tokens: limite de tokens da resposta.
        temperature: aleatoriedade (0.3 = respostas consistentes).

    Returns:
        Texto da resposta do modelo, ja com strip().
    """
    mensagens = []
    if system:
        mensagens.append({"role": "system", "content": system})
    mensagens.append({"role": "user", "content": prompt})

    try:
        resposta = _client.chat(
            model="gpt-oss:120b",
            messages=mensagens,
            options={
                "num_predict": max_tokens,
                "temperature": temperature,
            },
            stream=False,
        )
        return resposta["message"]["content"].strip()
    except Exception as e:
        return f"[ERRO] Falha ao consultar Ollama Cloud: {e}"


def _carregar_system_prompt() -> str:
    """Le o system prompt de prompts/system_prompt.md."""
    caminho = Path("prompts/system_prompt.md")
    if caminho.exists():
        return caminho.read_text(encoding="utf-8")
    # Fallback minimo caso o arquivo esteja faltando
    return (
        "Voce e o Mission Control AI, assistente de telemetria de "
        "satelite GNSS. Responda com diagnostico tecnico breve."
    )


class MissionEngine:
    """
    Motor de analise da missao MobilitySat.

    Mantem memoria de contexto entre chamadas (lista de leituras recentes)
    para que o LLM possa observar tendencias - implementa o diferencial
    'memoria de contexto' mencionado no briefing.
    """

    def __init__(self) -> None:
        self.trilha = TRILHA
        self.system_prompt = _carregar_system_prompt()
        self.historico_leituras: list[dict] = []
        self.tamanho_historico = 5  # mantem as ultimas N leituras

    def is_ready(self) -> bool:
        """Sistema esta pronto para responder."""
        return bool(os.environ.get("OLLAMA_API_KEY"))

    def status_snapshot(self) -> str:
        """
        Retorna um resumo textual da telemetria atual, sem chamar o LLM.
        Util para o comando /status da CLI - resposta instantanea.
        """
        leitura = telemetria.coletar()
        avaliacao = alertas.avaliar(leitura)
        self._registrar_no_historico(leitura, avaliacao)

        linhas = [
            f"Trilha           : MobilitySat (GNSS / Mobilidade)",
            f"Ciclo            : #{leitura['ciclo']}",
            f"Modo operacional : {leitura['modo_operacional']}",
            f"Severidade       : {avaliacao['nivel']}",
            "",
            f"Drift atomico    : {leitura['drift_atomico_ns']} ns/dia",
            f"Satelites vis.   : {leitura['satelites_visiveis']}",
            f"SNR canal L1     : {leitura['integridade_l1_db']} dB-Hz",
            f"SNR canal L5     : {leitura['integridade_l5_db']} dB-Hz",
            f"Margem potencia  : {leitura['margem_potencia_dbm']} dBm",
        ]

        if avaliacao["alertas"]:
            linhas.append("")
            linhas.append("Alertas ativos:")
            for alerta in avaliacao["alertas"]:
                linhas.append(f"  - {alerta}")

        if avaliacao["acao_automatizada"]:
            linhas.append("")
            linhas.append(
                f"Acao automatica : {avaliacao['acao_automatizada']}"
            )

        return "\n".join(linhas)

    def analyze(self, pergunta_usuario: str,
                cenario_forcado: str | None = None) -> str:
        """
        Analise principal: combina telemetria + alertas + IA.

        Args:
            pergunta_usuario: pergunta livre do operador.
            cenario_forcado: se 'nominal' / 'atencao' / 'critico',
                             gera cenario controlado em vez de aleatorio.
                             Usado pelos comandos especiais da CLI.
        """
        # 1. Coletar telemetria (real ou cenario controlado)
        if cenario_forcado:
            leitura = telemetria.gerar_cenario(cenario_forcado)
        else:
            leitura = telemetria.coletar()

        # 2. Avaliar alertas em CODIGO PYTHON (nao no LLM)
        avaliacao = alertas.avaliar(leitura)

        # 3. Registrar no historico de contexto
        self._registrar_no_historico(leitura, avaliacao)

        # 4. Construir prompt dinamico com dados reais injetados
        prompt = self._construir_prompt(pergunta_usuario, leitura, avaliacao)

        # 5. Chamar o LLM com system prompt customizado
        return llm(
            prompt=prompt,
            system=self.system_prompt,
            max_tokens=800,
            temperature=0.3,
        )

    # ========================================================
    # Metodos privados
    # ========================================================

    def _registrar_no_historico(self, leitura: dict,
                                  avaliacao: dict) -> None:
        """Mantem janela deslizante das ultimas N leituras."""
        self.historico_leituras.append({
            "leitura": leitura,
            "avaliacao": avaliacao,
        })
        if len(self.historico_leituras) > self.tamanho_historico:
            self.historico_leituras.pop(0)

    def _construir_prompt(self, pergunta: str, leitura: dict,
                          avaliacao: dict) -> str:
        """
        Constroi o prompt do usuario com todos os dados da telemetria
        injetados dinamicamente - este e o ponto que diferencia
        'IA decorativa' (prompt estatico) de 'IA integrada com dados'.
        """
        contexto = f"""# CONTEXTO OPERACIONAL DO SATELITE

**Trilha:** MobilitySat (GNSS - Mobilidade e Logistica)
**Timestamp:** {leitura['timestamp']}
**Ciclo de telemetria:** #{leitura['ciclo']}
**Modo operacional do satelite:** {leitura['modo_operacional']}

## Telemetria atual

- Drift do oscilador atomico: **{leitura['drift_atomico_ns']} ns/dia**
- Satelites visiveis: **{leitura['satelites_visiveis']}**
- SNR canal L1 (1575.42 MHz): **{leitura['integridade_l1_db']} dB-Hz**
- SNR canal L5 (1176.45 MHz): **{leitura['integridade_l5_db']} dB-Hz**
- Margem de potencia: **{leitura['margem_potencia_dbm']} dBm**

## Severidade calculada pelo sistema

**{avaliacao['nivel']}**
"""

        if avaliacao["alertas"]:
            contexto += "\n## Alertas detectados\n\n"
            for a in avaliacao["alertas"]:
                contexto += f"- {a}\n"

        if avaliacao["acao_automatizada"]:
            contexto += (
                f"\n## Acao automatizada ja executada pelo sistema\n\n"
                f"{avaliacao['acao_automatizada']}\n"
            )

        # Janela de tendencia se houver historico
        if len(self.historico_leituras) > 1:
            tendencia = self._resumir_tendencia()
            if tendencia:
                contexto += f"\n## Tendencia recente\n\n{tendencia}\n"

        contexto += f"\n---\n\n## Pergunta do operador\n\n{pergunta}\n"

        return contexto

    def _resumir_tendencia(self) -> str:
        """
        Gera resumo de 1-2 linhas sobre como os parametros vem
        evoluindo nas ultimas leituras - alimenta memoria de contexto.
        """
        if len(self.historico_leituras) < 2:
            return ""

        primeiro = self.historico_leituras[0]["leitura"]
        ultimo = self.historico_leituras[-1]["leitura"]
        delta_drift = ultimo["drift_atomico_ns"] - primeiro["drift_atomico_ns"]
        delta_sats = ultimo["satelites_visiveis"] - primeiro["satelites_visiveis"]

        partes = []
        if abs(delta_drift) > 0.5:
            direcao = "crescendo" if delta_drift > 0 else "decrescendo"
            partes.append(
                f"drift atomico {direcao} ({delta_drift:+.2f} ns "
                f"nas ultimas {len(self.historico_leituras)} leituras)"
            )
        if abs(delta_sats) >= 2:
            direcao = "aumentou" if delta_sats > 0 else "diminuiu"
            partes.append(f"visibilidade de satelites {direcao}")

        if not partes:
            return "Parametros estaveis nas ultimas leituras."
        return "Nas ultimas leituras: " + ", ".join(partes) + "."
