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
    columnas_export = ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA', 'Unnamed: 40']
    columnas_TC = ['Fecha', 'Valor', 'CuentaIva/13250055']
    columnas_import = ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA', 'Unnamed: 48']

    try:
        # Leer los archivos de Excel
        df_f43 = pd.read_excel(excel_f43, sheet_name='Acreedores SAP', usecols=columnas_f43)
        
        
        df_exportaciones = pd.read_excel(opera_export, sheet_name="ENERO", usecols=columnas_export)
        # # Leer todas las hojas excepto 'DATA'
        # sheets = pd.read_excel(opera_export, sheet_name=None)
        # sheets.pop('DATA', None)  # Eliminar la hoja 'DATA' si existe
        # print(df_exportaciones.columns)
        # df_exportaciones = pd.concat([df[columnas_export] for df in sheets.values()], ignore_index=True)

        df_TC = pd.read_excel(excel_TC, sheet_name='TC', usecols=columnas_TC)
        df_importaciones = pd.read_excel(opera_import, sheet_name='CONCENTRADO ANUAL 2025', usecols=columnas_import)

    except Exception as e:
        print(f"Error al leer los datos: {e}")
        return None, None


    return df_f43, df_exportaciones, df_TC, df_importaciones
