"""
Mission Control AI - Ponto de entrada do sistema.

Trilha escolhida: MobilitySat (GNSS / Mobilidade e Logistica)
Disciplina: Prompt Engineering and Artificial Intelligence
FIAP - Global Solution 2026.1
"""
from src.ui import run_cli
from src.engine import MissionEngine


if __name__ == "__main__":
    engine = MissionEngine()
    run_cli(engine)
