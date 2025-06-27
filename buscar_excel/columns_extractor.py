import pandas as pd
import sys
import os
import json

def extraer_columnas(config_file="config.json"):
    with open(config_file, "r") as f:
        config = json.load(f)

    # Rutas
    excel_f43 = config["EXCEL_F43"]
    opera_export = config["EXCEL_EXPORT"]
    opera_import = config["EXCEL_IMPORT"]
    excel_TC = config["EXCEL_TC"]

    # Columnas a extraer
    columnas_f43 = ['Cta CP (SAP)', 'Denominacion cuenta contrapartida', 'Centro coste', 'Cl coste']
    columnas_export = [1, 25, 29, 31, 34, 37, 44]
    columnas_TC = ['Fecha', 'Valor', 'CuentaIva/13250055']
    columnas_import = [1, 20, 30, 33, 37, 39, 43, 47]

    try:
        # Leer los archivos de Excel
        df_f43 = pd.read_excel(excel_f43, sheet_name='Acreedores SAP', usecols=columnas_f43)


        df_exportaciones = pd.read_excel(opera_export, sheet_name="EXPO", usecols=columnas_export)
        print(df_exportaciones)
        # # Leer todas las hojas excepto 'DATA'
        # sheets = pd.read_excel(opera_export, sheet_name=None)
        # sheets.pop('DATA', None)  # Eliminar la hoja 'DATA' si existe
        # print(df_exportaciones.columns)
        # df_exportaciones = pd.concat([df[columnas_export] for df in sheets.values()], ignore_index=True)

        df_TC = pd.read_excel(excel_TC, sheet_name='TC', usecols=columnas_TC)
        df_importaciones = pd.read_excel(opera_import, sheet_name='OPERACIONES 2025', usecols=columnas_import)

    except Exception as e:
        print(f"Error al leer los datos: {e}")
        return None, None, None, None

    # if df_exportaciones is not None:
    #     print("\nColumnas del DataFrame de Exportaciones:")
    #     print(df_exportaciones.columns.tolist())

    # if df_importaciones is not None:
    #     print("\nColumnas del DataFrame de Importaciones:")
    #     print(df_importaciones.columns.tolist())

    return df_f43, df_exportaciones, df_TC, df_importaciones