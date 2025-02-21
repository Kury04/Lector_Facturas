import pandas as pd
import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from buscar_excel.columns_extractor import extraer_columnas
from xml_procesador.procesador import procesar_documentos

def buscar_columnas(carpeta, progress_bar):
    archivos = os.listdir(carpeta)
    total_archivos = len(archivos) if archivos else 1  # Evitar división por cero
    progreso = 0

    # Procesar documentos y extraer columnas
    df_facturas, df_palabras = procesar_documentos(carpeta)
    df_f43, df_exportaciones, df_TC, df_importaciones = extraer_columnas()

    # Eliminar duplicados
    df_facturas = df_facturas.drop_duplicates(subset=['Archivo'])
    df_importaciones = df_importaciones.drop_duplicates(subset=['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])
    df_exportaciones = df_exportaciones.drop_duplicates(subset=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])

    # Actualizar progreso
    progreso += 1
    progress_bar.set(progreso / total_archivos)

    # Función para limpiar y normalizar datos
    def limpiar_dataframe(df, columnas):
        for col in columnas:
            df[col] = df[col].astype(str).str.strip().str.upper()
        return df

    df_f43 = limpiar_dataframe(df_f43, ["Denominacion cuenta contrapartida"])
    df_facturas = limpiar_dataframe(df_facturas, ["nombre_emisor", "Folio"])
    df_palabras = limpiar_dataframe(df_palabras, ["nombre_emisor", "Invoice"])
    df_exportaciones = limpiar_dataframe(df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])
    df_importaciones = limpiar_dataframe(df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])

    progreso += 1
    progress_bar.set(progreso / total_archivos)

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
                    break
        return df_left

    df_palabras = busqueda_secuencial(df_palabras, 'Invoice', df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'], 'Unnamed: 40')
    df_facturas = busqueda_secuencial(df_facturas, 'Folio', df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'], 'Unnamed: 48')

    progreso += 1
    progress_bar.set(progreso / total_archivos)

    # Realizar merges
    df1_FF = pd.merge(df_facturas, df_f43, how='left', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
    df3_FX = pd.merge(df_palabras, df_f43, how='left', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')

    df_palabras_tc = pd.merge(df_palabras, df_TC, on="Fecha", how="left")
    df_palabras_tc.loc[~df_palabras_tc["nombre_emisor"].isin(["C.H. ROBINSON COMPANY, INC", "SOLUTRANS LOGISTICS S,A"]), ["Valor", "CuentaIva/13250055"]] = None

    df_nacionales = pd.concat([df1_FF, df_facturas])
    df_extranjeros = pd.concat([df_exportaciones, df3_FX])

    df_extranjeros_completa = pd.merge(df_extranjeros, df_palabras_tc, on='nombre_emisor', how="left")
    df_extranjeros_completa = df_extranjeros_completa.drop_duplicates()

    df_prueba = pd.concat([df_extranjeros_completa, df_palabras_tc], axis=0)
    df_prueba = df_prueba.drop_duplicates(subset=['Invoice'], ignore_index=True)
    df_prueba.replace("", np.nan, inplace=True)
    df_prueba = df_prueba.dropna(axis=1, how='all')

    progreso += 1
    progress_bar.set(progreso / total_archivos)

    # Guardar resultados en Excel
    output_path = os.path.join(carpeta, "Datos_Unificados.xlsx")
    with pd.ExcelWriter(output_path) as writer:
        df_nacionales = df_nacionales.drop(columns=['Denominacion cuenta contrapartida'])
        df_nacionales = df_nacionales.drop_duplicates(subset=['Folio'])
        # df_nacionales = df_nacionales[df_nacionales.isna().sum(axis=1) <= 2]

        df_prueba = df_prueba.drop(columns=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA', 'Unnamed: 40_x'])
        df_palabras_tc = df_palabras_tc[df_palabras_tc.isna().sum(axis=1) <= 2]

        df_nacionales.to_excel(writer, index=False, sheet_name="XML")
        df_prueba.to_excel(writer, index=False, sheet_name="PDFs")

        print("PROCESO TERMINADO CON EXITO!!")


    progreso += 1
    progress_bar.set(1)
    
    return df_nacionales, df_palabras_tc
