# ============================================================
# utils/formatter.py — Formatea y muestra la tabla en terminal
# ============================================================

import sys
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from scrapers.base_scraper import Producto

# Consola con soporte UTF-8 explícito
console = Console(force_terminal=True, legacy_windows=False)


def mostrar_tabla(termino: str, productos: list[Producto]) -> None:
    """Muestra una tabla comparativa de productos ordenada por precio total."""

    if not productos:
        console.print("\n[bold red]❌ No se encontraron resultados en ninguna tienda.[/bold red]")
        return

    # Ordenar por total ascendente
    productos_ordenados = sorted(productos, key=lambda p: p.total)

    table = Table(
        title=f'\n🛒 Comparador de Precios — "[bold cyan]{termino}[/bold cyan]"',
        box=box.ROUNDED,
        show_lines=True,
        border_style="bright_blue",
        header_style="bold white on dark_blue",
    )

    table.add_column("#",         style="bold", width=3,  justify="center")
    table.add_column("Tienda",    style="bold cyan",  width=14, justify="center")
    table.add_column("Producto",  style="white",      width=45)
    table.add_column("Precio",    style="yellow",     width=10, justify="right")
    table.add_column("Envío",     style="dim white",  width=10, justify="right")
    table.add_column("TOTAL",     style="bold green", width=12, justify="right")
    table.add_column("Enlace",    style="blue",       width=8,  justify="center")

    medallas = {0: "🥇", 1: "🥈", 2: "🥉"}

    for i, prod in enumerate(productos_ordenados):
        pos = medallas.get(i, str(i + 1))

        # Colorear el total: verde si es el más barato, rojo si es el más caro
        if i == 0:
            total_str = Text(f"${prod.total:.2f}", style="bold green")
        elif i == len(productos_ordenados) - 1:
            total_str = Text(f"${prod.total:.2f}", style="bold red")
        else:
            total_str = Text(f"${prod.total:.2f}", style="white")

        envio_str = "GRATIS" if prod.envio == 0.0 else f"${prod.envio:.2f}"

        table.add_row(
            pos,
            prod.tienda,
            prod.nombre,
            f"${prod.precio:.2f}",
            envio_str,
            total_str,
            "[link=" + prod.url + "]Ver[/link]" if prod.url else "—",
        )

    console.print(table)

    # Resumen final
    mejor = productos_ordenados[0]
    peor  = productos_ordenados[-1]
    ahorro = peor.total - mejor.total

    console.print(
        f"\n💡 [bold]Mejor opción:[/bold] [green]{mejor.tienda}[/green] — "
        f"[bold green]${mejor.total:.2f}[/bold green]  |  "
        f"Ahorro vs. el más caro: [bold yellow]${ahorro:.2f}[/bold yellow]\n"
    )


def mostrar_progreso(tienda: str, estado: str) -> None:
    iconos = {"buscando": "🔍", "ok": "✅", "error": "❌", "bloqueado": "⚠️ "}
    icono = iconos.get(estado, "•")
    console.print(f"  {icono}  [dim]{tienda}...[/dim]")
