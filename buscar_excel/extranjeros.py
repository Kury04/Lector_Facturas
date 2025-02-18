import pandas as pd
import numpy as np

def limpiar_dataframe(df, columnas):
    """Función para limpiar y normalizar datos."""
    for col in columnas:
        df[col] = df[col].astype(str).str.strip().str.upper()
    return df

def procesar_extranjeros(df_palabras, df_exportaciones, df_TC):
    """Procesar datos extranjeros."""
    # Eliminar duplicados
    df_exportaciones = df_exportaciones.drop_duplicates(subset=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])

    # Limpieza y normalización de datos
    df_palabras = limpiar_dataframe(df_palabras, ["nombre_emisor", "Invoice"])
    df_exportaciones = limpiar_dataframe(df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])

    # Convertir fechas
    df_palabras["Fecha"] = pd.to_datetime(df_palabras["Fecha"], dayfirst=True, errors='coerce')
    df_TC["Fecha"] = pd.to_datetime(df_TC["Fecha"], dayfirst=True, errors='coerce')

    # Búsqueda secuencial
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

    df_palabras = busqueda_secuencial(
        df_palabras, 'Invoice', df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'], 'Unnamed: 40'
    )

    # Unión de datos con TC
    df_palabras_tc = pd.merge(df_palabras, df_TC, on="Fecha", how="left")
    df_palabras_tc.loc[~df_palabras_tc["nombre_emisor"].isin(["C.H. ROBINSON COMPANY, INC", "SOLUTRANS LOGISTICS S,A"]), ["Valor", "CuentaIva/13250055"]] = None

    # Combinar DataFrames
    df_extranjeros_completa = pd.merge(
        df_exportaciones, df_palabras_tc, on='nombre_emisor', how="left"
    )

    # Eliminar columnas innecesarias y duplicados
    df_extranjeros_completa = df_extranjeros_completa.drop(columns=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA', 'Archivo'])
    df_extranjeros_completa = df_extranjeros_completa.drop_duplicates(subset=['Invoice'])
    df_extranjeros_completa = df_extranjeros_completa[df_extranjeros_completa.isna().sum(axis=1) <= 3]

    return df_extranjeros_completa