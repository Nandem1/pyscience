import os
import re
import pdfplumber
import pandas as pd

def extraer_productos_pdf(ruta_pdf: str) -> pd.DataFrame:
    productos = []

    with pdfplumber.open(ruta_pdf) as pdf:
        texto = pdf.pages[0].extract_text()

        # Extraer número de documento
        documento_match = re.search(r'Documento N°(\d+)', texto)
        documento = documento_match.group(1) if documento_match else 'SIN_DOC'

        # Buscar total declarado en PDF
        total_match = re.search(r'Total \$\s?(\d+)', texto)
        total_extraido = int(total_match.group(1)) if total_match else 0

        # Sección de productos
        if "Productos Cantidad Precio Sub Total" not in texto:
            print(f"[AVISO] No se encontró sección de productos en {ruta_pdf}")
            return pd.DataFrame()

        texto_lineas = texto.split("Productos Cantidad Precio Sub Total")[-1]

        for linea in texto_lineas.strip().split("\n"):
            linea = linea.strip()

            if not linea or any(p in linea for p in ["Total", "Glosa"]):
                continue

            tokens = linea.split()
            if len(tokens) < 5:
                print(f"[OMITIDA] {os.path.basename(ruta_pdf)} ➞ '{linea}' (muy corta)")
                continue

            try:
                subtotal = float(tokens[-1].replace(",", "").replace(".", ""))
                precio_unitario = float(tokens[-2].replace(",", "").replace(".", ""))
                cantidad = int(tokens[-3])
                codigo = tokens[0]
                descripcion = " ".join(tokens[2:-3]) if tokens[1] == "-" else " ".join(tokens[1:-3])

                productos.append({
                    'Codigo': codigo,
                    'Descripcion': descripcion.strip(),
                    'Cantidad': cantidad,
                    'Precio': precio_unitario,
                    'Subtotal': subtotal,
                    'Documento': documento
                })
            except Exception as e:
                print(f"[ERROR] {os.path.basename(ruta_pdf)} ➞ '{linea}' ({e})")

    return pd.DataFrame(productos) if productos else pd.DataFrame()