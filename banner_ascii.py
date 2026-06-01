"""
Script auxiliar para gerar e testar o banner ASCII da Mission Control AI.

Uso:
    python banner_ascii.py                 # banner padrao em ciano e roxo
    python banner_ascii.py --fonts         # lista as 570+ fontes do pyfiglet
    python banner_ascii.py --font slant    # testa uma fonte especifica
    python banner_ascii.py --demo          # mostra 8 fontes lado a lado
"""

import argparse
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text


COR_PRIMARIA = "#06B6D4"
COR_SECUNDARIA = "#A855F7"
COR_TENUE = "#64748B"

# Selecao curada de fontes que renderizam bem no terminal padrao
FONTES_DEMO = [
    "ansi_shadow", "slant", "big", "doom",
    "standard", "small", "block", "isometric1",
]


def banner_padrao(console: Console) -> None:
    """Gera o banner oficial usado pela CLI."""
    linha1 = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("AI", font="ansi_shadow")

    console.print()
    console.print(
        Align.center(Text(linha1, style=f"bold {COR_PRIMARIA}"))
    )
    console.print(
        Align.center(Text(linha2, style=f"bold {COR_SECUNDARIA}"))
    )
    console.print(Align.center(Text(
        "Global Solution 2026.1  -  FIAP Ciencia da Computacao",
        style=f"italic {COR_TENUE}",
    )))
    console.print()


def listar_fontes(console: Console) -> None:
    """Lista todas as fontes do pyfiglet (sao mais de 570)."""
    fontes = sorted(pyfiglet.FigletFont.getFonts())
    console.print(f"[bold {COR_PRIMARIA}]Fontes disponiveis "
                  f"({len(fontes)} no total):[/]\n")
    largura = 28
    linha = ""
    for f in fontes:
        linha += f.ljust(largura)
        if len(linha) >= largura * 4:
            console.print(f"[{COR_TENUE}]{linha}[/]")
            linha = ""
    if linha:
        console.print(f"[{COR_TENUE}]{linha}[/]")


def testar_fonte(console: Console, fonte: str, texto: str) -> None:
    """Renderiza o texto em uma fonte especifica."""
    try:
        arte = pyfiglet.figlet_format(texto, font=fonte)
        console.print(f"[bold {COR_PRIMARIA}]Fonte: {fonte}[/]")
        console.print(Text(arte, style=f"bold {COR_PRIMARIA}"))
    except Exception as e:
        console.print(f"[red]Erro ao renderizar fonte '{fonte}': {e}[/]")


def demo_8_fontes(console: Console) -> None:
    """Renderiza 'Mission Control AI' em 8 fontes diferentes."""
    for fonte in FONTES_DEMO:
        console.print(f"\n[bold {COR_SECUNDARIA}]>>> {fonte}[/]\n")
        try:
            arte = pyfiglet.figlet_format("Mission AI", font=fonte)
            console.print(Text(arte, style=COR_PRIMARIA))
        except Exception:
            console.print(f"[red](fonte '{fonte}' indisponivel)[/]")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gerador de banner ASCII da Mission Control AI"
    )
    parser.add_argument(
        "--fonts", action="store_true",
        help="Lista todas as fontes do pyfiglet",
    )
    parser.add_argument(
        "--font", default=None,
        help="Renderiza o texto em uma fonte especifica",
    )
    parser.add_argument(
        "--text", default="Mission Control AI",
        help="Texto a ser renderizado",
    )
    parser.add_argument(
        "--demo", action="store_true",
        help="Mostra 8 fontes lado a lado",
    )

    args = parser.parse_args()
    console = Console()

    if args.fonts:
        listar_fontes(console)
    elif args.demo:
        demo_8_fontes(console)
    elif args.font:
        testar_fonte(console, args.font, args.text)
    else:
        banner_padrao(console)


if __name__ == "__main__":
    main()
