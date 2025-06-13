# 🖼️ Odoo Image Import

Script en Python para cargar imágenes masivamente a productos en **Odoo 16** a través de la API XML-RPC.

## 🚀 Funcionalidades

- Carga de imagen principal (`image_1920`) basada en nombre de archivo.
- Carga de múltiples imágenes adicionales (`product.image`) evitando duplicados.
- Validación básica de formato de imagen.
- Reporte de errores por imagen no válida o producto no encontrado.

## 🛠️ Requisitos

- Python 3.8+
- Odoo 16 (conectividad vía XML-RPC habilitada)
- Librerías Python:
  - `Pillow`
  - `xmlrpc.client` (builtin)
  - `base64` (builtin)

Instalación rápida:

```bash
pip install -r requirements.txt
