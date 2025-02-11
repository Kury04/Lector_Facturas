import pandas as pd
import sys
import os

def extraer_columnas():
    # Rutas
    excel_f43 = "resources/files/F-43.xlsx"
    opera_expor = "resources/files/OPERACIONES DE EXPORTACION 2025.xlsx"

    # Columnas a extraer
    columnas_f43 = ['Cta CP (SAP)', 'Denominacion cuenta contrapartida', 'Centro coste', 'Cl coste']
    columnas_operaciones = ['Unnamed: 14', 'Unnamed: 25', 'Unnamed: 40']

    try:
        # Leer los archivos de Excel
        df_f43 = pd.read_excel(excel_f43, sheet_name='Acreedores SAP', usecols=columnas_f43)
        df_operaciones = pd.read_excel(opera_expor, sheet_name='ENERO', usecols=columnas_operaciones)

    except Exception as e:
        print(f"Error al leer los datos: {e}")
        return None, None

    return df_f43, df_operaciones

extraer_columnas()