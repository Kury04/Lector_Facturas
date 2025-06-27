import numpy as np

def limpiar_dataframe(df, columnas):
    for col in columnas:
        df[col] = df[col].astype(str).str.strip().str.upper()
    return df

def busqueda_secuencial(df_left, col_left, df_importaciones, df_exportaciones, col_extra_importaciones, col_extra_exportaciones):
    df_left[col_extra_importaciones] = np.nan
    df_left[col_extra_exportaciones] = np.nan

    for index, row in df_left.iterrows():
        valor = row[col_left]
        print(f"\nBuscando el valor '{valor}' en df_importaciones y df_exportaciones...")

        for col in df_importaciones.columns:
            match = df_importaciones[df_importaciones[col] == valor]
            if not match.empty:
                df_left.at[index, col_extra_importaciones] = match.iloc[0][col_extra_importaciones]
                break

        for col in df_exportaciones.columns:
            match = df_exportaciones[df_exportaciones[col] == valor]
            if not match.empty:
                df_left.at[index, col_extra_exportaciones] = match.iloc[0][col_extra_exportaciones]
                break

    return df_left
