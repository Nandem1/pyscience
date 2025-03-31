import os
import pandas as pd
from pdf_extractor.extractor import extraer_productos_pdf
from pdf_extractor.validator import validar_documento

def procesar_carpeta_pdfs(ruta_carpeta: str) -> pd.DataFrame:
    df_total = pd.DataFrame()
    pdfs_procesados = 0
    pdfs_con_productos = 0

    for archivo in os.listdir(ruta_carpeta):
        if not archivo.lower().endswith(".pdf"):
            continue

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