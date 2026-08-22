# ============================================================
# config.py — Configuración central de PriceHunter
# ============================================================

# Tiendas habilitadas (True = activa, False = desactivada)
TIENDAS_ACTIVAS = {
    "mercadolibre": True,
    "ebay":         True,
    "aliexpress":   True,
    "amazon":       True,
    "shein":        True,
}

# Número máximo de resultados a mostrar por tienda
MAX_RESULTADOS_POR_TIENDA = 5

# Tiempo máximo de espera por tienda (segundos)
TIMEOUT_SEGUNDOS = 30

# Moneda de visualización
MONEDA = "USD"

# País para MercadoLibre
# Opciones: MLA=Argentina, MLM=Mexico, MLC=Chile, MLV=Venezuela, MCO=Colombia
MERCADOLIBRE_SITE = "MLM"  # México (más productos disponibles)

# Directorio de salida para archivos exportados
DIRECTORIO_OUTPUT = "output"

# Nombre del archivo de historial
ARCHIVO_HISTORIAL = "output/historial.json"
