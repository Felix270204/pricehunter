# ============================================================
# main.py — Punto de entrada de PriceHunter
# ============================================================

import sys
import os
import argparse
import asyncio

# Forzar codificación UTF-8 en Windows para caracteres especiales y emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console

from config import TIENDAS_ACTIVAS, MAX_RESULTADOS_POR_TIENDA, TIMEOUT_SEGUNDOS
from scrapers import (
    ShoppingAggregatorScraper,
    MercadoLibreScraper,
    EbayScraper,
    AliExpressScraper,
    AmazonScraper,
    SheinScraper,
    Producto,
)
from utils import (
    mostrar_tabla,
    console,
    exportar_a_excel,
    guardar_historial,
)


def banner():
    console.print(
        Panel.fit(
            "[bold cyan]🛒 PriceHunter[/bold cyan] — [yellow]Comparador de Precios Multi-Tienda[/yellow]\n"
            "[dim]Extracción automatizada con Python: MercadoLibre | eBay | AliExpress | Shein | Amazon[/dim]",
            border_style="bright_blue",
        )
    )


async def buscar_en_tienda(nombre: str, scraper_cls, termino: str, limite: int, timeout: int) -> tuple[str, list[Producto]]:
    """Ejecuta el scraper de una tienda con manejo seguro de excepciones."""
    try:
        scraper = scraper_cls(max_resultados=limite, timeout=timeout)
        resultados = await scraper.buscar(termino)
        return nombre, resultados
    except Exception as e:
        return nombre, []


async def ejecutar_busqueda(termino: str, limite: int, exportar: bool) -> None:
    banner()

    # Mapeo de tiendas
    tiendas_lista = ["AliExpress", "eBay", "Amazon", "Shein", "MercadoLibre"]
    tiendas_a_ejecutar = [t for t in tiendas_lista if TIENDAS_ACTIVAS.get(t.lower(), False)]

    console.print(f"\n🔍 Buscando [bold cyan]'{termino}'[/bold cyan] en [bold]{len(tiendas_a_ejecutar)} tiendas[/bold] en paralelo...\n")

    todos_los_productos: list[Producto] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Consultando plataformas y comparando ofertas...", total=None)

        tareas = [
            ShoppingAggregatorScraper(tienda_objetivo=tienda, max_resultados=limite, timeout=TIMEOUT_SEGUNDOS).buscar(termino)
            for tienda in tiendas_a_ejecutar
        ]
        resultados_tiendas = await asyncio.gather(*tareas)

    # Mostrar resumen por tienda
    for prods in resultados_tiendas:
        if prods:
            tienda_nombre = prods[0].tienda
            console.print(f"  [green]✔[/green] [bold]{tienda_nombre}:[/bold] [green]{len(prods)}[/green] ofertas procesadas")
            todos_los_productos.extend(prods)

    # Mostrar tabla enriquecida
    mostrar_tabla(termino, todos_los_productos)

    # Guardar en historial siempre
    if todos_los_productos:
        guardar_historial(termino, todos_los_productos)

    # Exportar a Excel si se solicitó o por defecto
    if exportar and todos_los_productos:
        ruta_excel = exportar_a_excel(termino, todos_los_productos)
        console.print(f"📊 [bold green]Reporte Excel generado con éxito:[/bold green] [underline]{ruta_excel}[/underline]\n")


def main():
    parser = argparse.ArgumentParser(
        description="PriceHunter: Comparador automatizado de precios en múltiples tiendas online."
    )
    parser.add_argument(
        "termino",
        type=str,
        nargs="?",
        default="iPhone 15",
        help="Nombre del producto a buscar (ej: 'Logitech G502', 'Teclado mecanico')",
    )
    parser.add_argument(
        "--limite",
        "-l",
        type=int,
        default=MAX_RESULTADOS_POR_TIENDA,
        help=f"Máximo de resultados por tienda (default: {MAX_RESULTADOS_POR_TIENDA})",
    )
    parser.add_argument(
        "--no-excel",
        action="store_true",
        help="Deshabilita la generación automática del archivo Excel",
    )

    args = parser.parse_args()

    # Ejecutar loop asíncrono
    asyncio.run(
        ejecutar_busqueda(
            termino=args.termino,
            limite=args.limite,
            exportar=not args.no_excel,
        )
    )


if __name__ == "__main__":
    main()
