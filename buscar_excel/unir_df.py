import pandas as pd
import os
from columns_extractor import extraer_columnas
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from xml_procesador.procesador import procesar_documentos

def buscar_columnas():
    carpeta = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/2025"
    df_facturas, df_palabras = procesar_documentos(carpeta)
    df_f43, df_exportaciones, df_TC, df_importaciones = extraer_columnas()

    # Eliminar duplicados antes de cualquier otra operación
    df_facturas = df_facturas.drop_duplicates(subset=['Archivo'])
    df_importaciones = df_importaciones.drop_duplicates(subset=['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])
    df_exportaciones = df_exportaciones.drop_duplicates(subset=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])
    
    # Limpieza y normalización de datos
    def limpiar_dataframe(df, columnas):
        for col in columnas:
            df[col] = df[col].astype(str).str.strip().str.upper()
        return df

    df_f43 = limpiar_dataframe(df_f43, ["Denominacion cuenta contrapartida"])
    df_facturas = limpiar_dataframe(df_facturas, ["nombre_emisor", "Folio"])
    df_palabras = limpiar_dataframe(df_palabras, ["nombre_emisor", "Invoice"])
    df_exportaciones = limpiar_dataframe(df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])
    df_importaciones = limpiar_dataframe(df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])
    
    # Convertir fechas antes de hacer merges
    df_palabras["Fecha"] = pd.to_datetime(df_palabras["Fecha"], dayfirst=True, errors='coerce')
    df_TC["Fecha"] = pd.to_datetime(df_TC["Fecha"], dayfirst=True, errors='coerce')
    
    def busqueda_secuencial(df_left, col_left, df_right, cols_right, col_extra):
        df_left[col_extra] = np.nan
        for index, row in df_left.iterrows():
            valor = row[col_left]
            for col in cols_right:
                match = df_right[df_right[col] == valor]
                if not match.empty:
                    df_left.at[index, col_extra] = match.iloc[0][col_extra]
                    break  # Detenerse en la primera coincidencia
        return df_left

    df_palabras = busqueda_secuencial(
        df_palabras, 'Invoice', df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'], 'Unnamed: 40'
    )

    df_facturas = busqueda_secuencial(
        df_facturas, 'Folio', df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'], 'Unnamed: 48'
    )
    
    # Merges optimizados
    df1_FF = pd.merge(df_facturas, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
    df3_FX = pd.merge(df_palabras, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
    
    df_nacionales = pd.concat([df1_FF, df_facturas])
    df_extranjeros = pd.concat([df_exportaciones, df3_FX])
    
    # Unión de datos con TC
    df_palabras_tc = pd.merge(df_palabras, df_TC, on="Fecha", how="left")
    df_palabras_tc.loc[~df_palabras_tc["nombre_emisor"].isin(["C.H. ROBINSON COMPANY, INC", "SOLUTRANS LOGISTICS S,A"]), ["Valor", "CuentaIva/13250055"]] = None

    df_nacionales_completa = pd.concat([df_nacionales, df_palabras_tc], ignore_index=True)
    # Eliminar duplicados en el DataFrame consolidado
    df_nacionales_completa = df_nacionales_completa.drop_duplicates()

    # Guardado en Excel
    output_path = "./resources/files/datos_unidos.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        df_extranjeros = df_extranjeros.drop(columns=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA', 'Archivo', 'Denominacion cuenta contrapartida'])
        df_extranjeros = df_extranjeros[df_extranjeros.isna().sum(axis=1) <= 3]

        df_nacionales_completa = df_nacionales.drop(columns=['Denominacion cuenta contrapartida'])
        df_palabras_tc = df_palabras_tc.drop(columns=['Archivo'])
        df_palabras_tc = df_palabras_tc[df_palabras_tc.isna().sum(axis=1) <= 3]

        df_nacionales_completa.to_excel(writer, index=False, sheet_name="Nacionales")
        df_extranjeros.to_excel(writer, index=False, sheet_name="Extranjeros")
        df_palabras_tc.to_excel(writer, index=False, sheet_name="TC")

buscar_columnas()