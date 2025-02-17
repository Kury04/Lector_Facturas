import pandas as pd
import os
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from columns_extractor import extraer_columnas
from xml_procesador.procesador import procesar_documentos



def buscar_columnas():
    carpeta = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/2025"
    df_facturas, df_palabras = procesar_documentos(carpeta)
    df_f43, df_exportaciones, df_TC, df_importaciones = extraer_columnas()

    # Limpieza y normalización de datos
    def limpiar_dataframe(df, columnas):
        for col in columnas:
            df[col] = df[col].astype(str).str.strip().str.upper()
        return df

    def busqueda_secuencial(df_left, col_left, df_right, cols_right, col_extra):
        """Optimización de búsqueda secuencial utilizando mapeo en lugar de iteración."""
        df_right_dict = df_right.set_index(cols_right[0])[col_extra].to_dict()
        df_left[col_extra] = df_left[col_left].map(df_right_dict)
        return df_left

    # Eliminar duplicados antes de cualquier otra operación
    df_facturas.drop_duplicates(subset=['Archivo'], inplace=True)
    df_importaciones.drop_duplicates(subset=['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'], inplace=True)
    df_exportaciones.drop_duplicates(subset=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'], inplace=True)

    # Limpieza de datos
    df_f43 = limpiar_dataframe(df_f43, ["Denominacion cuenta contrapartida"])
    df_facturas = limpiar_dataframe(df_facturas, ["nombre_emisor", "Folio"])
    df_palabras = limpiar_dataframe(df_palabras, ["nombre_emisor", "Invoice"])
    df_exportaciones = limpiar_dataframe(df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])
    df_importaciones = limpiar_dataframe(df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])

    # Convertir fechas antes de hacer merges
    df_palabras["Fecha"] = pd.to_datetime(df_palabras["Fecha"], dayfirst=True, errors='coerce')
    df_TC["Fecha"] = pd.to_datetime(df_TC["Fecha"], dayfirst=True, errors='coerce')

    # Aplicar búsqueda secuencial optimizada
    df_palabras = busqueda_secuencial(df_palabras, 'Invoice', df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'], 'Unnamed: 40')
    df_facturas = busqueda_secuencial(df_facturas, 'Folio', df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'], 'Unnamed: 48')

    # Unión de datos con TC
    df_palabras_tc = df_palabras.merge(df_TC, on="Fecha", how="left")
    df_palabras_tc.loc[~df_palabras_tc["nombre_emisor"].isin(["C.H. ROBINSON COMPANY, INC", "SOLUTRANS LOGISTICS S,A"]), 
                       ["Valor", "CuentaIva/13250055"]] = None

    # Merges para nacionales
    df_nacionales_completa = df_facturas.merge(df_f43, how='outer', 
                                               left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
    df_nacionales_completa.drop_duplicates(subset=['Archivo', 'Folio'], inplace=True)

    # Merges para extranjeros
    df_extranjeros_completa = df_palabras.merge(df_f43, how='outer', 
                                                left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
    df_extranjeros_completa = pd.concat([df_exportaciones, df_extranjeros_completa], ignore_index=True)
    df_extranjeros_completa.drop_duplicates(subset=['Invoice', 'Archivo'], inplace=True)

    if not df_palabras_tc.empty:
        df_extranjeros_completa = pd.concat([df_extranjeros_completa, df_palabras_tc], ignore_index=True)
        df_extranjeros_completa.drop_duplicates(subset=['Invoice', 'Archivo'], inplace=True)

    # Guardado en Excel
    output_path = "./resources/files/datos_unidos.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        df_extranjeros_completa.drop(columns=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA', 'Archivo', 'Denominacion cuenta contrapartida'], errors='ignore').to_excel(writer, index=False, sheet_name="Extranjeros")
        df_nacionales_completa.drop(columns=['Denominacion cuenta contrapartida', 'Archivo', 'Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'], errors='ignore').to_excel(writer, index=False, sheet_name="Nacionales")

buscar_columnas()
