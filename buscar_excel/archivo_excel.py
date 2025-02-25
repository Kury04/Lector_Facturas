import os
import pandas as pd
import numpy as np

def guardar_resultados(df_nacionales, df_prueba, carpeta):
    output_path = os.path.join(carpeta, "Datos_Unificados.xlsx")

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        if not df_nacionales.empty:
            # Eliminar columnas no deseadas
            df_nacionales = df_nacionales.drop(columns=['Denominacion cuenta contrapartida'], errors='ignore')
            df_nacionales = df_nacionales.drop_duplicates(subset=['Folio'])

            # Renombrar columnas
            df_nacionales.rename(columns={'Unnamed: 40': 'REF SAP EXPO', 'Unnamed: 48': 'REF SAP IMPO'}, inplace=True)

            # Exportar a Excel
            df_nacionales.to_excel(writer, index=False, sheet_name="XML")

        if not df_prueba.empty:
            # Eliminar columnas no deseadas
            df_prueba = df_prueba.drop(columns=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA', 'Unnamed: 40_x'], errors='ignore')

            # Renombrar columnas
            df_prueba.rename(columns={'Unnamed: 40': 'REF SAP EXPO', 'Unnamed: 48': 'REF SAP IMPO'}, inplace=True)

            # Definir el orden de las columnas
            orden_columnas_prueba = [
                'ID','nombre_emisor','TAX ID','Invoice','Fecha','Moneda','Total','RFC_Receptor','Archivo','REF SAP EXPO', 'REF SAP IMPO' # Columnas principales
            ]

            # Reorganizar el DataFrame
            df_prueba = df_prueba[orden_columnas_prueba]

            # Exportar a Excel
            df_prueba.to_excel(writer, index=False, sheet_name="PDFs")

        # Si no hay datos en ningún DataFrame, crear una hoja vacía con un mensaje
        if len(writer.book.sheetnames) == 0:
            pd.DataFrame({"Mensaje": ["No hay datos disponibles"]}).to_excel(writer, index=False, sheet_name="HojaVacia")