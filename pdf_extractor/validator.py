import pandas as pd

def validar_documento(df: pd.DataFrame, total_esperado: int, archivo_pdf: str) -> None:
    errores = []

    # Validación de total
    if 'Subtotal' in df.columns:
        total_calculado = df['Subtotal'].sum()
        if abs(total_calculado - total_esperado) > 1:
            errores.append(
                f"[TOTAL] Diferencia en total del documento {archivo_pdf}: extraído = {total_calculado}, PDF = {total_esperado}"
            )

    # Validación de campos
    for i, fila in df.iterrows():
        if not str(fila['Descripcion']).strip():
            errores.append(f"[CAMPO VACÍO] Fila {i+1} sin descripción en {archivo_pdf}")
        if not str(fila['Codigo']).isdigit():
            errores.append(f"[CÓDIGO INVÁLIDO] Fila {i+1} código '{fila['Codigo']}' en {archivo_pdf}")
        if int(fila['Cantidad']) <= 0:
            errores.append(f"[CANTIDAD INVÁLIDA] Fila {i+1} cantidad '{fila['Cantidad']}' en {archivo_pdf}")

    # Mostrar errores en consola
    if errores:
        print(f"\n🔠 Validaciones fallidas en {archivo_pdf}:")
        for err in errores:
            print("  ", err)
    else:
        print(f"[VALIDACIÓN OK] {archivo_pdf}")

    # Guardar en archivo de log
    if errores:
        with open("validacion.log", "a", encoding="utf-8") as log:
            log.write(f"\n==== {archivo_pdf} ====")
            for err in errores:
                log.write(f"{err}\n")
