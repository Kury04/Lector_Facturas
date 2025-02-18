import pandas as pd
import numpy as np

def limpiar_dataframe(df, columnas):
    """Función para limpiar y normalizar datos."""
    for col in columnas:
        df[col] = df[col].astype(str).str.strip().str.upper()
    return df

def procesar_nacionales(df_facturas, df_f43, df_importaciones):
    """Procesar datos nacionales."""
    # Eliminar duplicados
    df_facturas = df_facturas.drop_duplicates(subset=['Archivo'])
    df_importaciones = df_importaciones.drop_duplicates(subset=['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'])

    # Limpieza y normalización de datos
    df_f43 = limpiar_dataframe(df_f43, ["Denominacion cuenta contrapartida"])
    df_facturas = limpiar_dataframe(df_facturas, ["nombre_emisor", "Folio"])

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

    df_facturas = busqueda_secuencial(
        df_facturas, 'Folio', df_importaciones, ['Unnamed: 10', 'Unnamed: 20', 'Unnamed: 30', 'CUSTODIA'], 'Unnamed: 48'
    )

    # Realizar merge
    df_nacionales = pd.merge(df_facturas, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')

    # Eliminar columnas innecesarias y duplicados
    df_nacionales = df_nacionales.drop(columns=['Denominacion cuenta contrapartida', 'Archivo'])
    df_nacionales = df_nacionales.drop_duplicates(subset=['Folio'])
    df_nacionales = df_nacionales[df_nacionales.isna().sum(axis=1) <= 3]

    return df_nacionales