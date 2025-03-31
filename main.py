import pdfplumber
import pandas as pd
import re
import os
import openpyxl


def validar_documento(df, total_esperado, archivo_pdf):
    errores = []
    total_calculado = 0

    # Validación de total
    if 'Subtotal' in df.columns:
        total_calculado = df['Subtotal'].sum()
        if abs(total_calculado - total_esperado) > 1:
            errores.append(
                f"[TOTAL] Diferencia en total del documento {archivo_pdf}: extraído = {total_calculado}, PDF = {total_esperado}")

    # Validación de campos
    for i, fila in df.iterrows():
        if not fila['Descripcion'] or not str(fila['Descripcion']).strip():
            errores.append(
                f"[CAMPO VACÍO] Fila {i+1} sin descripción en {archivo_pdf}")
        if not str(fila['Codigo']).isdigit():
            errores.append(
                f"[CÓDIGO INVÁLIDO] Fila {i+1} código '{fila['Codigo']}' en {archivo_pdf}")
        if int(fila['Cantidad']) <= 0:
            errores.append(
                f"[CANTIDAD INVÁLIDA] Fila {i+1} cantidad '{fila['Cantidad']}' en {archivo_pdf}")

    # Mostrar en consola
    if errores:
        print(f"\n🔠 Validaciones fallidas en {archivo_pdf}:")
        for err in errores:
            print("  ", err)
    else:
        print(f"[VALIDACIÓN OK] {archivo_pdf}")

    # Escribir log
    if errores:
        log_path = "validacion.log"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n==== {archivo_pdf} ====")
            for err in errores:
                f.write(err + "\n")

def extraer_productos_pdf(ruta_pdf):
    productos = []
    total_extraido = 0

    with pdfplumber.open(ruta_pdf) as pdf:
        texto = pdf.pages[0].extract_text()

        # Extraer número de documento
        doc_match = re.search(r'Documento N°(\d+)', texto)
        documento = doc_match.group(1) if doc_match else 'SIN_DOC'

        # Extraer Total del PDF
        total_match = re.search(r'Total \$\s?(\d+)', texto)
        if total_match:
            total_extraido = int(total_match.group(1))

        # Extraer solo desde "Productos Cantidad Precio Sub Total"
        if "Productos Cantidad Precio Sub Total" in texto:
            texto_lineas = texto.split("Productos Cantidad Precio Sub Total")[-1]
        else:
            print(f"[AVISO] No se encontró sección 'Productos Cantidad Precio Sub Total' en {ruta_pdf}")
            return pd.DataFrame()

        for linea in texto_lineas.strip().split("\n"):
            linea = linea.strip()

            if not linea or "Total" in linea or "Glosa" in linea:
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

    if not productos:
        return pd.DataFrame()

    return pd.DataFrame(productos)

def procesar_carpeta_pdfs(ruta_carpeta):
    df_total = pd.DataFrame()
    pdfs_procesados = 0
    pdfs_con_productos = 0

    for archivo in os.listdir(ruta_carpeta):
        if archivo.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(ruta_carpeta, archivo)
            try:
                df_pdf = extraer_productos_pdf(ruta_pdf)
                pdfs_procesados += 1

                if not df_pdf.empty:
                    pdfs_con_productos += 1
                    df_total = pd.concat([df_total, df_pdf], ignore_index=True)
                    print(f"[OK] Productos extraídos desde: {archivo} ({len(df_pdf)} registros)")

                    total_pdf = int(df_pdf['Subtotal'].sum())
                    validar_documento(df_pdf, total_pdf, archivo)
                else:
                    print(f"[VACÍO] No se extrajo ningún producto de: {archivo}")

            except Exception as e:
                print(f"[ERROR] Fallo procesando {archivo}: {e}")

    print(f"\n✅ PDF procesados: {pdfs_procesados}")
    print(f"📦 Con productos extraídos: {pdfs_con_productos}")
    print(f"📄 Total de registros extraídos: {len(df_total)}")

    return df_total

ruta_carpeta = "pdf"
df_final = procesar_carpeta_pdfs(ruta_carpeta)
df_final.to_excel("productos_extraidos.xlsx", index=False)