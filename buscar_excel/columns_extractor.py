import pandas as pd
import sys
import os

def extraer_columnas():
    # Rutas
    excel_f43 = "resources/files/F-43.xlsx"
    opera_export = "resources/files/OPERACIONES DE EXPORTACION 2025.xlsx"
    opera_import= "resources/files/OPERACIONES DE IMPORTACION 2025.xlsx"
    excel_TC = "resources/files/TC.xlsx"

    # Columnas a extraer
    columnas_f43 = ['Cta CP (SAP)', 'Denominacion cuenta contrapartida', 'Centro coste', 'Cl coste']
    columnas_export = ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA', 'Unnamed: 40']
    columnas_TC = ['Fecha','Valor','CuentaIva/13250055']
    columnas_import = ['Unnamed: 10','Unnamed: 20','Unnamed: 30', 'CUSTODIA','Unnamed: 48']

    try:
        # Leer los archivos de Excel
        df_f43 = pd.read_excel(excel_f43, sheet_name='Acreedores SAP', usecols=columnas_f43)
        df_exportaciones = pd.read_excel(opera_export, sheet_name='ENERO' , usecols=columnas_export)
        df_TC = pd.read_excel(excel_TC, sheet_name='TC', usecols=columnas_TC)
        df_importaciones = pd.read_excel(opera_import, sheet_name='CONCENTRADO ANUAL 2025', usecols=columnas_import)

    except Exception as e:
        print(f"Error al leer los datos: {e}")
        return None, None

    return df_f43, df_exportaciones, df_TC, df_importaciones