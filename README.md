# 📦 PDF Extractor - Inventario Escolar

Este proyecto permite procesar múltiples archivos PDF que contienen información de productos (como mochilas, útiles, etc.) y extraer los datos relevantes para generar un archivo Excel con toda la información organizada.

> Diseñado con arquitectura limpia, modular y escalable. Ideal para trazabilidad de productos en cajas físicas, validación de datos y centralización de inventario.

---

## 🧠 ¿Qué hace este proyecto?

- Lee múltiples PDFs desde una carpeta.
- Extrae los productos listados en cada documento (código, descripción, cantidad, precio y subtotal).
- Valida campos vacíos, códigos inválidos y cantidades incorrectas.
- Compara la suma de subtotales con el total declarado en el PDF.
- Exporta los datos a un archivo Excel (`productos_extraidos.xlsx`).
- Guarda errores de validación en `validacion.log`.

---

## 📁 Estructura del proyecto

```bash
pdf_extractor/
├── main.py                      # Punto de entrada del sistema
├── pdf_extractor/
│   ├── __init__.py              # Indica que es un paquete Python
│   ├── processor.py             # Lógica para recorrer y procesar los PDFs
│   ├── extractor.py             # Lógica de extracción por archivo
│   └── validator.py             # Validaciones de campos y totales
```

---

## ⚙️ Cómo usar

1. Asegúrate de tener Python instalado (3.8+ recomendado).

2. Coloca tus archivos PDF dentro de una carpeta llamada `pdf/` al mismo nivel que `main.py`.

3. Ejecuta el script:

```bash
python main.py
```

4. Al finalizar, obtendrás:
   - `productos_extraidos.xlsx`: con todos los productos extraídos.
   - `validacion.log`: con los errores detectados, si existen.

---

## 🛠 Requisitos (solo si trabajas en entorno virtual)

```bash
pip install pandas pdfplumber openpyxl
```

---

## 🧼 Buenas prácticas aplicadas

- Clean Code & Modularización
- Tipado de funciones y nombres claros
- Manejo de errores y validaciones
- Logging de errores persistente (`validacion.log`)
- Estructura lista para testing, escalamiento o integración futura

---

## 💡 Ideas futuras

- Agregar CLI para elegir carpeta o archivo destino
- Exportación en formatos CSV o base de datos
- Dashboard con gráficos por producto o caja
- Soporte multi-página o multi-línea por PDF

---

## ✍️ Autor

Este proyecto fue creado y refactorizado con arquitectura profesional por iniciativa del usuario ✨

¿Quieres colaborar o escalarlo a una app web o API? ¡Adelante! 😄
