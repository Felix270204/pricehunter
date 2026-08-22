# ============================================================
# scrapers/base_scraper.py — Clase base para todos los scrapers
# ============================================================

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Producto:
    """Representa un producto encontrado en una tienda."""
    tienda: str
    nombre: str
    precio: float
    envio: float
    total: float
    url: str
    moneda: str = "USD"
    disponible: bool = True
    imagen: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "tienda":      self.tienda,
            "nombre":      self.nombre,
            "precio":      self.precio,
            "envio":       self.envio,
            "total":       self.total,
            "url":         self.url,
            "moneda":      self.moneda,
            "disponible":  self.disponible,
        }


class BaseScraper:
    """
    Clase base que deben heredar todos los scrapers.
    Define la interfaz común y métodos de utilidad.
    """

    NOMBRE_TIENDA = "Tienda Base"

    def __init__(self, max_resultados: int = 5, timeout: int = 30):
        self.max_resultados = max_resultados
        self.timeout = timeout

    async def buscar(self, termino: str) -> list[Producto]:
        """
        Busca un producto y retorna una lista de Producto.
        Debe ser implementado por cada scraper hijo.
        """
        raise NotImplementedError("Cada scraper debe implementar el método buscar()")

    def _limpiar_precio(self, texto: str) -> float:
        """Convierte un texto de precio a float. Ej: '$1,234.56' → 1234.56"""
        if not texto:
            return 0.0
        # Eliminar símbolos de moneda y espacios
        limpio = texto.strip()
        for char in ["$", "€", "£", "¥", "MXN", "USD", ",", " ", "\xa0"]:
            limpio = limpio.replace(char, "")
        # Manejar punto como separador decimal
        try:
            return float(limpio)
        except ValueError:
            return 0.0

    def _truncar_nombre(self, nombre: str, max_len: int = 60) -> str:
        """Limpia saltos de línea y trunca el nombre del producto si es muy largo."""
        if not nombre:
            return "Producto"
        # Eliminar saltos de línea, retornos de carro y múltiples espacios
        limpio = " ".join(nombre.split())
        # Remover etiquetas comunes como 'Ad' o 'Anuncio'
        for prefijo in ["Ad ", "Anuncio ", "Sponsored "]:
            if limpio.startswith(prefijo):
                limpio = limpio[len(prefijo):]
        if len(limpio) > max_len:
            return limpio[:max_len - 3] + "..."
        return limpio
