import pandas as pd
import numpy as np

def procesar_nacionales(df_facturas, df_f43):
    # Limpiar y normalizar datos
    df_f43 = limpiar_dataframe(df_f43, ["Denominacion cuenta contrapartida"])
    df_facturas = limpiar_dataframe(df_facturas, ["nombre_emisor", "Folio"])

    # Realizar merge
    df_nacionales = pd.merge(df_facturas, df_f43, how='left', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
    df_nacionales = df_nacionales.drop(columns=['Denominacion cuenta contrapartida'], errors='ignore')
    df_nacionales = df_nacionales.drop_duplicates(subset=['Folio'])

    return df_nacionales

def limpiar_dataframe(df, columnas):
    for col in columnas:
        df[col] = df[col].astype(str).str.strip().str.upper()
    return df