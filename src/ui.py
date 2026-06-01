"""
Interface CLI estilo Claude Code para a Mission Control AI.

Implementada com:
    - Rich (paineis, cores, tabelas, formatacao markdown)
    - prompt-toolkit (input editavel com historico e estilizacao)
    - pyfiglet (banner ASCII art)

Comandos suportados:
    /help                - lista os comandos disponiveis
    /status              - resumo da telemetria atual (sem chamar IA)
    /cenario nominal     - forca cenario nominal e analisa
    /cenario atencao     - forca cenario de atencao e analisa
    /cenario critico     - forca cenario critico e analisa
    /about               - sobre o projeto e a equipe
    /clear               - limpa a tela e reexibe banner
    /exit                - encerra o sistema (ou Ctrl+C / Ctrl+D)
"""

from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from rich.align import Align

import pyfiglet
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style as PtkStyle


# ============================================================
# Configuracao visual
# ============================================================
console = Console()

# Paleta de cores estilo Claude Code (ciano + cinza escuro)
COR_PRIMARIA = "#06B6D4"      # ciano - destaques principais
COR_SECUNDARIA = "#A855F7"    # roxo - subtitulos
COR_ALERTA = "#F59E0B"        # ambar - atencao
COR_CRITICO = "#EF4444"       # vermelho - critico
COR_OK = "#10B981"            # verde - nominal
COR_TENUE = "#64748B"         # cinza - texto auxiliar

# Estilo do prompt de input
session = PromptSession(
    style=PtkStyle.from_dict({
        "prompt": f"{COR_PRIMARIA} bold",
    })
)


# ============================================================
# Componentes visuais
# ============================================================

def _mostrar_banner() -> None:
    """Exibe banner ASCII de abertura, centralizado e colorido."""
    banner = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    subtitulo = pyfiglet.figlet_format("AI", font="ansi_shadow")

    console.print()
    console.print(
        Align.center(Text(banner, style=f"bold {COR_PRIMARIA}"))
    )
    console.print(
        Align.center(Text(subtitulo, style=f"bold {COR_SECUNDARIA}"))
    )
    console.print(
        Align.center(Text(
            "Global Solution 2026.1  -  FIAP Ciencia da Computacao",
            style=f"italic {COR_TENUE}",
        ))
    )
    console.print()


def _mostrar_card_boas_vindas(engine) -> None:
    """Painel com instrucoes iniciais e estado do engine."""
    trilha_label = "MobilitySat (GNSS / Mobilidade e Logistica)"
    pronto = engine.is_ready()
    estado = (
        Text("ONLINE", style=f"bold {COR_OK}") if pronto
        else Text("API KEY AUSENTE", style=f"bold {COR_CRITICO}")
    )

    conteudo = Text.assemble(
        ("Trilha tematica:  ", "bold"),
        (trilha_label + "\n", COR_PRIMARIA),
        ("Modelo de IA:     ", "bold"),
        ("gpt-oss:120b via Ollama Cloud\n", COR_PRIMARIA),
        ("Status do engine: ", "bold"),
        estado,
        ("\n\n", ""),
        ("Comandos: ", "bold"),
        ("/help  /status  /cenario {nominal|atencao|critico}  /clear  /exit",
         COR_TENUE),
    )

    console.print(Panel(
        conteudo,
        title=f"[bold {COR_PRIMARIA}]Mission Control AI[/]",
        border_style=COR_PRIMARIA,
        padding=(1, 2),
    ))

    if not pronto:
        console.print(Panel(
            Text(
                "OLLAMA_API_KEY nao encontrada no arquivo .env. "
                "Crie o arquivo .env na raiz do projeto com a sua chave "
                "antes de iniciar consultas a IA.",
                style=COR_CRITICO,
            ),
            border_style=COR_CRITICO,
        ))


def _mostrar_resposta(texto: str, severidade: str | None = None) -> None:
    """
    Exibe a resposta da IA em um painel com borda colorida conforme a
    severidade do cenario (se conhecida) e timestamp no rodape.
    """
    agora = datetime.now().strftime("%H:%M:%S")

    cor_borda = COR_PRIMARIA
    if severidade == "CRITICO":
        cor_borda = COR_CRITICO
    elif severidade == "ATENCAO":
        cor_borda = COR_ALERTA
    elif severidade == "NORMAL":
        cor_borda = COR_OK

    console.print(Panel(
        Markdown(texto),
        title=f"[bold {cor_borda}]Mission Control AI[/]",
        subtitle=f"[{COR_TENUE}]{agora}[/]",
        border_style=cor_borda,
        padding=(1, 2),
    ))


def _mostrar_help() -> None:
    """Tabela com os comandos disponiveis."""
    tabela = Table(
        title=f"[bold {COR_PRIMARIA}]Comandos disponiveis[/]",
        border_style=COR_PRIMARIA,
        show_header=True,
        header_style=f"bold {COR_PRIMARIA}",
    )
    tabela.add_column("Comando", style="bold")
    tabela.add_column("Funcao")

    tabela.add_row("/help", "Lista os comandos disponiveis")
    tabela.add_row("/status", "Snapshot da telemetria atual sem chamar IA")
    tabela.add_row(
        "/cenario nominal", "Forca cenario de operacao nominal e pede analise"
    )
    tabela.add_row(
        "/cenario atencao", "Forca cenario de atencao e pede analise"
    )
    tabela.add_row(
        "/cenario critico", "Forca cenario critico e pede analise"
    )
    tabela.add_row("/about", "Sobre o projeto e a equipe")
    tabela.add_row("/clear", "Limpa a tela e reexibe o banner")
    tabela.add_row("/exit", "Encerra o sistema (Ctrl+C / Ctrl+D)")
    tabela.add_row(
        "<pergunta livre>",
        "Coleta nova telemetria e pede analise contextualizada da IA",
    )

    console.print(tabela)


def _mostrar_about() -> None:
    """Painel com informacoes do projeto e equipe."""
    conteudo = Text.assemble(
        ("Projeto:    ", "bold"),
        ("Mission Control AI - Trilha MobilitySat\n", COR_PRIMARIA),
        ("Disciplina: ", "bold"),
        ("Prompt Engineering and Artificial Intelligence\n", ""),
        ("Professor:  ", "bold"),
        ("Jorge Luiz Gomes\n", ""),
        ("Turma:      ", "bold"),
        ("1CCPH\n\n", ""),
        ("Integrantes:\n", "bold"),
        ("  - Joao Pedro do Vale Quagliano (RM 570233)\n", ""),
        ("  - Matheus Levi Dagel (RM 571961)\n\n", ""),
        ("Modelo de IA: ", "bold"),
        ("gpt-oss:120b via Ollama Cloud\n", COR_PRIMARIA),
        ("Stack:        ", "bold"),
        ("Python 3.10+ / Rich / prompt-toolkit / pyfiglet", COR_PRIMARIA),
    )
    console.print(Panel(
        conteudo,
        title=f"[bold {COR_PRIMARIA}]Sobre o projeto[/]",
        border_style=COR_PRIMARIA,
        padding=(1, 2),
    ))


# ============================================================
# Loop principal
# ============================================================

def run_cli(engine) -> None:
    """
    Loop principal da interface CLI.

    Recebe a instancia de MissionEngine e gerencia o ciclo de input,
    despachando cada comando ou pergunta livre para o motor.
    """
    _mostrar_banner()
    _mostrar_card_boas_vindas(engine)

    while True:
        try:
            entrada = session.prompt("> ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print(
                f"\n[{COR_TENUE}]Encerrando Mission Control AI...[/]"
            )
            break

        if not entrada:
            continue

        # ============== COMANDOS ESPECIAIS ==============

        if entrada == "/exit":
            console.print(
                f"[{COR_TENUE}]Encerrando Mission Control AI...[/]"
            )
            break

        if entrada == "/help":
            _mostrar_help()
            continue

        if entrada == "/about":
            _mostrar_about()
            continue

        if entrada == "/clear":
            console.clear()
            _mostrar_banner()
            _mostrar_card_boas_vindas(engine)
            continue

        if entrada == "/status":
            snapshot = engine.status_snapshot()
            console.print(Panel(
                Text(snapshot, style=COR_PRIMARIA),
                title=f"[bold {COR_PRIMARIA}]Telemetria atual[/]",
                border_style=COR_PRIMARIA,
                padding=(1, 2),
            ))
            continue

        # Comando /cenario {nominal|atencao|critico}
        if entrada.startswith("/cenario"):
            partes = entrada.split()
            if len(partes) != 2 or partes[1] not in (
                "nominal", "atencao", "critico"
            ):
                console.print(
                    f"[{COR_ALERTA}]Uso: /cenario "
                    "{nominal|atencao|critico}[/]"
                )
                continue
            severidade_solicitada = partes[1]
            pergunta_padrao = (
                "Como esta a missao? Faca o diagnostico completo "
                "para o engenheiro de plantao."
            )
            console.print(
                f"[{COR_TENUE}]Forcando cenario "
                f"'{severidade_solicitada}' e consultando IA...[/]"
            )
            with console.status(
                "[bold cyan]Mission Control AI processando...",
                spinner="dots",
            ):
                resposta = engine.analyze(
                    pergunta_padrao,
                    cenario_forcado=severidade_solicitada,
                )
            # Severidade real e o que veio do alerta (pode coincidir
            # com a solicitada se cenario for o esperado)
            sev_real = severidade_solicitada.upper()
            _mostrar_resposta(resposta, severidade=sev_real)
            continue

        # ============== PERGUNTA LIVRE ==============

        if not engine.is_ready():
            console.print(Panel(
                Text(
                    "Sistema sem credenciais. Configure o arquivo .env "
                    "com OLLAMA_API_KEY antes de fazer consultas.",
                    style=COR_CRITICO,
                ),
                border_style=COR_CRITICO,
            ))
            continue

        with console.status(
            "[bold cyan]Mission Control AI processando...",
            spinner="dots",
        ):
            resposta = engine.analyze(entrada)

        # Severidade vem do ultimo registro do historico
        ultima = engine.historico_leituras[-1] if engine.historico_leituras \
            else None
        severidade = ultima["avaliacao"]["nivel"] if ultima else None

        _mostrar_resposta(resposta, severidade=severidade)
