"""
Telemetria simulada do satelite GNSS (MobilitySat).

Este modulo simula a leitura de cinco parametros criticos de um satelite
de navegacao por satelite (GNSS) em orbita media (MEO, ~20.000 km),
similar a um satelite das constelacoes GPS Block IIIA, Galileo FOC ou
GLONASS-K.

Parametros monitorados:
    1. drift_atomico_ns      - drift do oscilador atomico (nanossegundos/dia)
    2. satelites_visiveis    - quantos satelites estao em linha de visada
    3. integridade_l1        - SNR do canal civil L1 (dB-Hz)
    4. integridade_l5        - SNR do canal de seguranca L5 (dB-Hz)
    5. margem_potencia_dbm   - margem de potencia do transmissor (dBm)

Cada chamada a coletar() retorna um snapshot da telemetria. Para a
demonstracao do video, ha tambem gerar_cenario(nivel) que forca cenarios
extremos (nominal, atencao, critico) usados pelos comandos especiais
da CLI.
"""

import random
from datetime import datetime
from typing import Literal


# ============================================================
# CONSTANTES DE OPERACAO NOMINAL
# ============================================================
# Valores baseados em especificacoes publicas de satelites GNSS reais.
# As faixas refletem operacao normal vs degradada vs critica.

# Drift do oscilador atomico - relogios de Cesio/Rubidio embarcados
# Operacao nominal: < 4 ns/dia. Drift > 10 ns/dia ja compromete precisao.
DRIFT_NOMINAL_MAX = 4.0
DRIFT_ATENCAO_MAX = 8.0

# Satelites visiveis - minimo de 4 para trilateracao 3D
SATELITES_NOMINAL_MIN = 7
SATELITES_ATENCAO_MIN = 5

# SNR (Signal-to-Noise Ratio) dos canais L1 (1575.42 MHz) e L5 (1176.45 MHz)
# Valores tipicos: 40-50 dB-Hz em ceu aberto. Abaixo de 35: sinal degradado.
SNR_NOMINAL_MIN = 42.0
SNR_ATENCAO_MIN = 37.0

# Margem de potencia do transmissor - quanto acima do minimo o sinal chega
# Operacao nominal: > 6 dB de margem. Abaixo de 3 dB: alerta.
POTENCIA_NOMINAL_MIN = 6.0
POTENCIA_ATENCAO_MIN = 3.0


# ============================================================
# ESTADO INTERNO DO SATELITE (memoria entre leituras)
# ============================================================
# Mantemos algumas variaveis acumulando ao longo do tempo para simular
# um satelite real - o relogio atomico nao "reseta" a cada leitura,
# ele acumula drift ao longo das horas e dias em orbita.

_estado_interno = {
    "drift_acumulado": 1.2,           # ns/dia inicial
    "ciclos_desde_calibracao": 0,     # contador de leituras
    "ultima_leitura": None,
    "modo_operacional": "NOMINAL",    # NOMINAL / DEGRADADO / SEGURANCA
}


def _aplicar_modo_operacional(valor_nominal: float, modo: str) -> float:
    """
    Aplica modulacao no valor conforme o modo operacional do satelite.
    Em modo de seguranca (apos alerta), o satelite ativa redundancias
    e a telemetria comeca a se recuperar.
    """
    if modo == "DEGRADADO":
        return valor_nominal * 1.5
    if modo == "SEGURANCA":
        return valor_nominal * 1.1
    return valor_nominal


def coletar() -> dict:
    """
    Coleta uma leitura instantanea da telemetria do satelite.

    Retorna um dicionario com os cinco parametros monitorados,
    o timestamp ISO 8601 e o modo operacional atual.

    Esta funcao tem memoria - chamadas consecutivas mostram o drift
    do oscilador atomico acumulando ao longo do tempo, simulando
    um satelite real em operacao continua.
    """
    global _estado_interno

    _estado_interno["ciclos_desde_calibracao"] += 1
    modo = _estado_interno["modo_operacional"]

    # Drift atomico cresce lentamente ao longo dos ciclos (simula deriva real)
    incremento_drift = random.uniform(0.05, 0.25)
    _estado_interno["drift_acumulado"] += incremento_drift
    drift = _aplicar_modo_operacional(_estado_interno["drift_acumulado"], modo)

    # Satelites visiveis - geralmente entre 6 e 12 em ceu aberto
    satelites = random.randint(7, 12)
    if modo == "DEGRADADO":
        satelites = random.randint(3, 6)

    # SNR dos canais L1 e L5 - flutuam com pequenas variacoes
    snr_l1 = round(random.uniform(42.0, 49.0), 2)
    snr_l5 = round(random.uniform(43.0, 48.0), 2)
    if modo == "DEGRADADO":
        snr_l1 = round(random.uniform(30.0, 36.0), 2)
        snr_l5 = round(random.uniform(31.0, 36.0), 2)

    # Margem de potencia do transmissor
    margem = round(random.uniform(6.5, 9.0), 2)
    if modo == "DEGRADADO":
        margem = round(random.uniform(2.0, 4.5), 2)

    leitura = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "ciclo": _estado_interno["ciclos_desde_calibracao"],
        "modo_operacional": modo,
        "drift_atomico_ns": round(drift, 2),
        "satelites_visiveis": satelites,
        "integridade_l1_db": snr_l1,
        "integridade_l5_db": snr_l5,
        "margem_potencia_dbm": margem,
    }

    _estado_interno["ultima_leitura"] = leitura
    return leitura


def gerar_cenario(nivel: Literal["nominal", "atencao", "critico"]) -> dict:
    """
    Forca a geracao de um cenario especifico para demonstracao.

    Util durante a apresentacao para mostrar como o sistema reage
    em cada situacao sem depender de aleatoriedade.

    Args:
        nivel: 'nominal' (tudo OK), 'atencao' (degradacao parcial)
               ou 'critico' (multiplas falhas simultaneas).

    Returns:
        Dicionario com a telemetria forcada.
    """
    global _estado_interno

    base = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "ciclo": _estado_interno["ciclos_desde_calibracao"] + 1,
    }
    _estado_interno["ciclos_desde_calibracao"] += 1

    if nivel == "nominal":
        base.update({
            "modo_operacional": "NOMINAL",
            "drift_atomico_ns": 2.1,
            "satelites_visiveis": 11,
            "integridade_l1_db": 47.5,
            "integridade_l5_db": 46.8,
            "margem_potencia_dbm": 7.8,
        })

    elif nivel == "atencao":
        base.update({
            "modo_operacional": "NOMINAL",
            "drift_atomico_ns": 6.4,
            "satelites_visiveis": 6,
            "integridade_l1_db": 39.2,
            "integridade_l5_db": 44.5,
            "margem_potencia_dbm": 4.8,
        })

    else:  # critico
        base.update({
            "modo_operacional": "DEGRADADO",
            "drift_atomico_ns": 12.7,
            "satelites_visiveis": 4,
            "integridade_l1_db": 31.5,
            "integridade_l5_db": 33.8,
            "margem_potencia_dbm": 2.4,
        })

    _estado_interno["ultima_leitura"] = base
    return base


def ativar_modo(modo: Literal["NOMINAL", "DEGRADADO", "SEGURANCA"]) -> None:
    """
    Altera o modo operacional do satelite (chamado pela resposta automatizada
    do modulo de alertas quando uma situacao critica e detectada).
    """
    global _estado_interno
    _estado_interno["modo_operacional"] = modo


def obter_estado_interno() -> dict:
    """Retorna o estado interno do satelite (para debug e CLI /status)."""
    return dict(_estado_interno)
