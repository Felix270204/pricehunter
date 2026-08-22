# 🕷️ PriceHunter — E-Commerce Web Scraper & Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

> **Aplicación Web Full-Stack y Motor de Extracción de Datos en Tiempo Real** para la búsqueda, comparación y análisis de catálogos y precios en más de 24 tiendas de comercio electrónico independientes.

---

## 🌟 Características Principales

- **⚡ Extracción Concurrente de Alto Rendimiento:** Motor asíncrono con `ThreadPoolExecutor` que consulta simultáneamente múltiples tiendas en paralelo en cuestión de segundos.
- **🔗 Enlaces y Datos 100% Reales:** Conexión directa con endpoints de catálogo para extraer títulos oficiales, precios de lista, variantes con descuento, imágenes en alta definición y URLs directas a la ficha de compra.
- **🌐 Traductor Bilingüe Inteligente (ES ➡️ EN):** Permite a los usuarios buscar indistintamente en español o en inglés (ej: *zapatos deportivos*, *camisas*, *funda*, *mochila*) mapeando términos a las estructuras de catálogo internacionales.
- **🎨 Interfaz Web Interactiva y Moderna:** Diseñada con **Tailwind CSS**, soporte para alternar entre vista en tarjetas con fotos HD y tabla comparativa detallada.
- **🎛️ Filtros Avanzados en Vivo:** Filtrado dinámico por categoría y selector deslizante (slider) de rango de precio mínimo y máximo en tiempo real.
- **📊 Exportación Automatizada a Microsoft Excel:** Generador integrado con `openpyxl` que produce hojas de cálculo estilizadas con fórmulas de ahorro y enlaces clickeables.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnologías |
| :--- | :--- |
| **Backend** | Python 3, Flask, REST API, Concurrency (`concurrent.futures`) |
| **Scraping / Data** | Requests, HTTP Endpoints, JSON parsing, `openpyxl` |
| **Frontend** | HTML5, Tailwind CSS, FontAwesome 6, JavaScript Vanilla |
| **Arquitectura** | Modular (Scrapers, API Controllers, Export Utilities) |

---

## 📂 Estructura del Proyecto

```text
pricehunter/
│
├── app.py                      # Servidor backend Flask y endpoints de la API
├── config.py                   # Configuraciones globales y rutas
├── requirements.txt            # Dependencias del proyecto
│
├── scrapers/
│   ├── __init__.py
│   └── shopify_scraper.py      # Motor de extracción concurrente multi-tienda
│
├── utils/
│   ├── __init__.py
│   └── exporter.py             # Generador de reportes en Excel (.xlsx)
│
├── templates/
│   └── index.html              # Frontend interactivo con Tailwind CSS
│
└── output/                     # Reportes generados y archivos de exportación
```

---

## 🚀 Instalación y Uso Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU-USUARIO/pricehunter.git
cd pricehunter
```

### 2. Crear entorno virtual (Recomendado)
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar la aplicación
```bash
python app.py
```

Abre tu navegador en: **`http://127.0.0.1:5000`**

---

## 👤 Autor

**Felix Roberto Borges Romero**  
*Desarrollador Web & Automatización en Python*  
- [Perfil de GitHub](https://github.com/)
- [Contacto en Workana](https://www.workana.com/)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
