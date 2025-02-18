import pandas as pd
import os
import sys
import numpy as np
# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from buscar_excel.columns_extractor import extraer_columnas
from xml_procesador.procesador import procesar_documentos

def buscar_columnas(carpeta):

    # Procesar documentos y extraer columnas
    df_facturas, df_palabras = procesar_documentos(carpeta)
    df_f43, df_exportaciones, df_TC, df_importaciones = extraer_columnas()

    # Eliminar duplicados
    df_facturas = df_facturas.drop_duplicates(subset=['Archivo'])
    df_importaciones = df_importaciones.drop_duplicates(subset=['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])
    df_exportaciones = df_exportaciones.drop_duplicates(subset=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])
    
    # Función para limpiar y normalizar datos
    def limpiar_dataframe(df, columnas):
        for col in columnas:
            df[col] = df[col].astype(str).str.strip().str.upper()
        return df

    # Limpieza y normalización de datos
    df_f43 = limpiar_dataframe(df_f43, ["Denominacion cuenta contrapartida"])
    df_facturas = limpiar_dataframe(df_facturas, ["nombre_emisor", "Folio"])
    df_palabras = limpiar_dataframe(df_palabras, ["nombre_emisor", "Invoice"])
    df_exportaciones = limpiar_dataframe(df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])
    df_importaciones = limpiar_dataframe(df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])
    
    # Convertir fechas
    df_palabras["Fecha"] = pd.to_datetime(df_palabras["Fecha"], dayfirst=True, errors='coerce')
    df_TC["Fecha"] = pd.to_datetime(df_TC["Fecha"], dayfirst=True, errors='coerce')
    
    # Función para búsqueda secuencial
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

    # Aplicar búsqueda secuencial
    df_palabras = busqueda_secuencial(
        df_palabras, 'Invoice', df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'], 'Unnamed: 40'
    )

    df_facturas = busqueda_secuencial(
        df_facturas, 'Folio', df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'], 'Unnamed: 48'
    )
    
    # Realizar merges
    df1_FF = pd.merge(df_facturas, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
    df3_FX = pd.merge(df_palabras, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')

    
    # Unión de datos con TC
    df_palabras_tc = pd.merge(df_palabras, df_TC, on="Fecha", how="left")
    df_palabras_tc.loc[~df_palabras_tc["nombre_emisor"].isin(["C.H. ROBINSON COMPANY, INC", "SOLUTRANS LOGISTICS S,A"]), ["Valor", "CuentaIva/13250055"]] = None

    # Concatenar DataFrames
    df_nacionales = pd.concat([df1_FF, df_facturas])
    df_extranjeros = pd.concat([df_exportaciones, df3_FX])

    # Añadir la columna "Valor" de df_palabras_tc_filtrado a df_extranjeros
    df_extranjeros_completa = pd.merge(
        df_extranjeros,
        df_palabras_tc,
        on='nombre_emisor',
        how="left"
    )

    df_extranjeros_completa = df_extranjeros_completa.drop_duplicates()
    # Unir df_extranjeros_completa con df_palabras_tc
    df_prueba = pd.concat([df_extranjeros_completa, df_palabras_tc], axis=0)  # Concatenar por filas
    df_prueba = df_prueba.drop_duplicates(subset=['Invoice'], ignore_index=True)
    # Eliminar columnas vacías (donde todos los valores son NaN)
    df_prueba.replace("", np.nan, inplace=True)
    df_prueba = df_prueba.dropna(axis=1, how='all')


    # Guardar resultados en Excel
    output_path = os.path.join(carpeta, "Datos_Unificados.xlsx")
    with pd.ExcelWriter(output_path) as writer:

        df_nacionales = df_nacionales.drop(columns=['Denominacion cuenta contrapartida','Archivo'])
        df_nacionales = df_nacionales.drop_duplicates(subset=['Folio'])
        df_nacionales = df_nacionales[df_nacionales.isna().sum(axis=1) <= 3]
        

        df_extranjeros_completa = df_extranjeros.drop(columns=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA','Archivo', 'Denominacion cuenta contrapartida'])
        df_extranjeros_completa = df_extranjeros_completa.drop_duplicates(subset=['Invoice'])
        df_extranjeros_completa = df_extranjeros_completa[df_extranjeros_completa.isna().sum(axis=1) <= 3]

        df_palabras_tc = df_palabras_tc[df_palabras_tc.isna().sum(axis=1) <= 3]

        df_nacionales.to_excel(writer, index=False, sheet_name="XML")
        df_prueba.to_excel(writer, index=False, sheet_name="PDFs")

        return df_nacionales, df_extranjeros_completa, df_palabras_tc