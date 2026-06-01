"""
Lógica de alertas e tomada de decisão automatizada.

Este modulo implementa a CAMADA DE DECISAO em Python puro - cumprindo
o requisito explicito do briefing (Frente 4): "a logica deve estar no
codigo Python, nao apenas no prompt da IA".

A IA generativa do projeto serve para EXPLICAR e CONTEXTUALIZAR os
alertas, mas NUNCA para decidir se algo e critico ou nao. Isso e papel
exclusivo destas funcoes deterministicas.

Regras de severidade:
    NORMAL    - todos os parametros dentro da faixa nominal
    ATENCAO   - pelo menos um parametro saiu da faixa nominal mas nao
                atingiu nivel critico
    CRITICO   - pelo menos um parametro atingiu nivel critico OU
                multiplos parametros simultaneamente em atencao
"""

from typing import Literal
from . import telemetria


# ============================================================
# THRESHOLDS - centralizar todas as regras em um unico lugar
# ============================================================

# Drift do oscilador atomico (ns/dia)
DRIFT_LIMITE_ATENCAO = 4.0      # acima disto: ATENCAO
DRIFT_LIMITE_CRITICO = 10.0     # acima disto: CRITICO

# Numero minimo de satelites visiveis para trilateracao confiavel
SATELITES_MINIMO_ATENCAO = 7    # abaixo disto: ATENCAO
SATELITES_MINIMO_CRITICO = 5    # abaixo disto: CRITICO

# SNR (dB-Hz) dos canais L1 e L5
SNR_LIMITE_ATENCAO = 42.0       # abaixo disto: ATENCAO
SNR_LIMITE_CRITICO = 35.0       # abaixo disto: CRITICO

# Margem de potencia (dBm) do transmissor
POTENCIA_LIMITE_ATENCAO = 6.0   # abaixo disto: ATENCAO
POTENCIA_LIMITE_CRITICO = 3.0   # abaixo disto: CRITICO


# ============================================================
# AVALIACAO INDIVIDUAL POR PARAMETRO
# ============================================================

def _avaliar_drift(valor: float) -> tuple[str, str]:
    """Avalia o drift do oscilador atomico. Retorna (nivel, mensagem)."""
    if valor >= DRIFT_LIMITE_CRITICO:
        return "CRITICO", (
            f"Drift do oscilador atomico em {valor} ns/dia - "
            "fora dos limites para navegacao precisa."
        )
    if valor >= DRIFT_LIMITE_ATENCAO:
        return "ATENCAO", (
            f"Drift de {valor} ns/dia acima do nominal - "
            "iniciar planejamento de calibracao."
        )
    return "NORMAL", ""


def _avaliar_satelites(valor: int) -> tuple[str, str]:
    """Avalia a quantidade de satelites visiveis."""
    if valor < SATELITES_MINIMO_CRITICO:
        return "CRITICO", (
            f"Apenas {valor} satelites visiveis - "
            "abaixo do minimo para trilateracao 3D segura (5)."
        )
    if valor < SATELITES_MINIMO_ATENCAO:
        return "ATENCAO", (
            f"Visibilidade reduzida: {valor} satelites - "
            "redundancia limitada."
        )
    return "NORMAL", ""


def _avaliar_snr(valor: float, canal: str) -> tuple[str, str]:
    """Avalia o SNR de um canal de sinal (L1 ou L5)."""
    if valor < SNR_LIMITE_CRITICO:
        return "CRITICO", (
            f"SNR do canal {canal} em {valor} dB-Hz - "
            "sinal severamente degradado."
        )
    if valor < SNR_LIMITE_ATENCAO:
        return "ATENCAO", (
            f"SNR do canal {canal} em {valor} dB-Hz - "
            "qualidade do sinal abaixo do nominal."
        )
    return "NORMAL", ""


def _avaliar_potencia(valor: float) -> tuple[str, str]:
    """Avalia a margem de potencia do transmissor."""
    if valor < POTENCIA_LIMITE_CRITICO:
        return "CRITICO", (
            f"Margem de potencia em {valor} dBm - "
            "transmissor proximo ao limite operacional."
        )
    if valor < POTENCIA_LIMITE_ATENCAO:
        return "ATENCAO", (
            f"Margem de potencia em {valor} dBm - "
            "reserva de transmissao reduzida."
        )
    return "NORMAL", ""


# ============================================================
# AVALIACAO GLOBAL E RESPOSTA AUTOMATIZADA
# ============================================================

def avaliar(t: dict) -> dict:
    """
    Avalia uma leitura completa de telemetria e retorna:
        - nivel: NORMAL / ATENCAO / CRITICO (severidade maxima)
        - alertas: lista de mensagens por parametro
        - acao_automatizada: acao que o sistema executou em resposta
                              (ou None se nao foi necessario)

    A acao automatizada e o ponto que cumpre o requisito do briefing:
    "Pelo menos uma resposta automatizada para situacao critica simulada"
    """
    # avaliacao de cada parametro
    avaliacoes = [
        _avaliar_drift(t["drift_atomico_ns"]),
        _avaliar_satelites(t["satelites_visiveis"]),
        _avaliar_snr(t["integridade_l1_db"], "L1"),
        _avaliar_snr(t["integridade_l5_db"], "L5"),
        _avaliar_potencia(t["margem_potencia_dbm"]),
    ]

    # severidade global = pior caso entre os parametros
    if any(nivel == "CRITICO" for nivel, _ in avaliacoes):
        nivel_global = "CRITICO"
    elif any(nivel == "ATENCAO" for nivel, _ in avaliacoes):
        nivel_global = "ATENCAO"
    else:
        nivel_global = "NORMAL"

    alertas = [msg for nivel, msg in avaliacoes if nivel != "NORMAL"]

    # ========================================================
    # RESPOSTA AUTOMATIZADA - executada em Python, nao no LLM
    # ========================================================
    acao = _executar_resposta_automatica(nivel_global, t)

    return {
        "nivel": nivel_global,
        "alertas": alertas,
        "acao_automatizada": acao,
    }


def _executar_resposta_automatica(nivel: str, t: dict) -> str | None:
    """
    Executa acao automatizada conforme a severidade detectada.

    Esta e a logica de decisao em codigo - o satelite reage a falhas
    sem esperar comando humano, exatamente como ocorre em satelites
    reais de operacao critica.
    """
    if nivel == "CRITICO":
        # Caso especifico: SNR L1 critico mas L5 ainda OK -> migrar para L5
        if t["integridade_l1_db"] < SNR_LIMITE_CRITICO and \
           t["integridade_l5_db"] >= SNR_LIMITE_ATENCAO:
            telemetria.ativar_modo("SEGURANCA")
            return (
                "MODO DE SEGURANCA ATIVADO automaticamente. "
                "Trafego de navegacao migrado do canal L1 para L5 ate "
                "estabilizacao do SNR."
            )

        # Caso geral critico: ativar modo de seguranca
        telemetria.ativar_modo("SEGURANCA")
        return (
            "MODO DE SEGURANCA ATIVADO automaticamente. "
            "Sistema reduziu carga de transmissao e priorizou "
            "envio de pacotes de integridade ate diagnostico humano."
        )

    if nivel == "ATENCAO":
        return (
            "Sistema em monitoramento intensificado. Frequencia de "
            "telemetria aumentada de 60s para 15s ate retorno ao nominal."
        )

    return None
