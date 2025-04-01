from pdf_extractor.processor import procesar_carpeta_pdfs
import pandas as pd


def main():
    ruta_pdfs = "pdf"
    df_final = procesar_carpeta_pdfs(ruta_pdfs)

    if not df_final.empty:
        output_file = "productos_extraidos.xlsx"
        df_final.to_excel(output_file, index=False)
        print(f"\n📁 Exportación completada: {output_file}")
    else:
        print("\n⚠️ No se extrajeron productos de ningún PDF.")


if __name__ == "__main__":
    main()