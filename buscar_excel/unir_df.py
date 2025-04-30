import os
import sys
import pandas as pd
import numpy as np
from openpyxl import load_workbook

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from buscar_excel.columns_extractor import extraer_columnas
from xml_procesador.procesador import procesar_documentos
from buscar_excel.procesamiento import limpiar_dataframe, busqueda_secuencial
from buscar_excel.archivo_excel import guardar_resultados

def buscar_columnas(carpeta, progress_bar):
    archivos = os.listdir(carpeta)
    total_archivos = len(archivos) if archivos else 1
    progreso = 0

    df_facturas, df_palabras = procesar_documentos(carpeta)
    df_f43, df_exportaciones, df_TC, df_importaciones = extraer_columnas()

    df_facturas = df_facturas.drop_duplicates(subset=['Archivo'])
    # df_importaciones = df_importaciones.drop_duplicates(subset=['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])
    # df_exportaciones = df_exportaciones.drop_duplicates(subset=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])

    progreso += 1
    progress_bar.set(progreso / total_archivos)

    df_f43 = limpiar_dataframe(df_f43, ["Denominacion cuenta contrapartida"])
    df_facturas = limpiar_dataframe(df_facturas, ["nombre_emisor", "Folio"])
    df_palabras = limpiar_dataframe(df_palabras, ["nombre_emisor", "Invoice"])
    # df_exportaciones = limpiar_dataframe(df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])
    # df_importaciones = limpiar_dataframe(df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])

    progreso += 1
    progress_bar.set(progreso / total_archivos)

    df_palabras["Fecha"] = pd.to_datetime(df_palabras["Fecha"], dayfirst=True, errors='coerce')
    df_TC["Fecha"] = pd.to_datetime(df_TC["Fecha"], dayfirst=True, errors='coerce')

    for col in ['INGRESO', 'Unnamed: 35']:
        if col not in df_exportaciones.columns:
            df_exportaciones[col] = np.nan
        if col not in df_importaciones.columns:
            df_importaciones[col] = np.nan


    df_palabras = busqueda_secuencial(df_palabras, 'Invoice', df_importaciones, df_exportaciones, 'Unnamed: 35', 'INGRESO')
    df_facturas = busqueda_secuencial(df_facturas, 'Folio', df_importaciones, df_exportaciones, 'Unnamed: 35', 'INGRESO')

    progreso += 1
    progress_bar.set(progreso / total_archivos)

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

    guardar_resultados(df_nacionales, df_prueba, carpeta)

    print("PROCESO TERMINADO CON ÉXITO!!")

    progreso += 1
    progress_bar.set(1)

    return df_nacionales, df_palabras_tc
