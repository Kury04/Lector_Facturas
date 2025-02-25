import pandas as pd
import numpy as np

def procesar_extranjeros(df_palabras, df_importaciones, df_exportaciones, df_TC):
    # Limpiar y normalizar datos
    df_palabras = limpiar_dataframe(df_palabras, ["nombre_emisor", "Invoice"])
    df_exportaciones = limpiar_dataframe(df_exportaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'])
    df_importaciones = limpiar_dataframe(df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])

    # Convertir fechas
    df_palabras["Fecha"] = pd.to_datetime(df_palabras["Fecha"], dayfirst=True, errors='coerce')
    df_TC["Fecha"] = pd.to_datetime(df_TC["Fecha"], dayfirst=True, errors='coerce')

    # Búsqueda secuencial
    df_palabras = busqueda_secuencial(df_palabras, 'Invoice', df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'], 'Unnamed: 48')

    # Realizar merge
    df_palabras_tc = pd.merge(df_palabras, df_TC, on="Fecha", how="left")
    df_palabras_tc.loc[~df_palabras_tc["nombre_emisor"].isin(["C.H. ROBINSON COMPANY, INC", "SOLUTRANS LOGISTICS S,A"]), ["Valor", "CuentaIva/13250055"]] = None

    df_extranjeros_completa = pd.merge(df_exportaciones, df_palabras_tc, on='nombre_emisor', how="left")
    df_extranjeros_completa = df_extranjeros_completa.drop_duplicates()

    return df_extranjeros_completa

def limpiar_dataframe(df, columnas):
    for col in columnas:
        df[col] = df[col].astype(str).str.strip().str.upper()
    return df

def busqueda_secuencial(df_left, col_left, df_right, cols_right, col_extra):
    df_left[col_extra] = np.nan  # Agrega una nueva columna con valores NaN

    for index, row in df_left.iterrows():
        valor = row[col_left]  # Valor de la columna a buscar
        for col in cols_right:
            match = df_right[df_right[col] == valor]  # Filtra coincidencias
            if not match.empty:
                df_left.at[index, col_extra] = match.iloc[0][col_extra]
                break  # Sale del loop si encuentra coincidencia

    return df_left