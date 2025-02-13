import pandas as pd
import os
import sys
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from xml_procesador.procesador import procesar_documentos
from buscar_excel.columns_extractor import extraer_columnas

def buscar_columnas():
    # Procesar los documentos en la carpeta especificada
    carpeta = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/2025"
    # carpeta = "./resources/files"

    # DATAFRAMES
    df_facturas, df_palabras = procesar_documentos(carpeta)
    df_f43, df_operaciones, df_TC  = extraer_columnas()

    # Normalizar claves de unión
    df_f43["Denominacion cuenta contrapartida"] = df_f43["Denominacion cuenta contrapartida"].str.strip().str.upper()
    df_facturas["nombre_emisor"] = df_facturas["nombre_emisor"].str.strip().str.upper()
    df_palabras["nombre_emisor"] = df_palabras["nombre_emisor"].str.strip().str.upper()
    df_facturas["Folio"] = df_facturas["Folio"].str.strip().str.upper()
    # Normalizar columnas clave en df_palabras
    df_palabras['Invoice'] = df_palabras['Invoice'].astype(str).str.strip().str.upper()

    # Normalizar columnas clave en df_operaciones
    df_operaciones['Unnamed: 14'] = df_operaciones['Unnamed: 14'].astype(str).str.strip().str.upper()
    df_operaciones['Unnamed: 25'] = df_operaciones['Unnamed: 25'].astype(str).str.strip().str.upper()
    df_operaciones['CUSTODIA'] = df_operaciones['CUSTODIA'].astype(str).str.strip().str.upper()
     
    print("Valores únicos en 'Invoice' (df_palabras):", df_palabras['Invoice'].unique())
    print("Valores únicos en 'Unnamed: 14' (df_operaciones):", df_operaciones['Unnamed: 14'].unique())
    print("Valores únicos en 'Unnamed: 25' (df_operaciones):", df_operaciones['Unnamed: 25'].unique())
    print("Valores únicos en 'CUSTODIA' (df_operaciones):", df_operaciones['CUSTODIA'].unique())

    # Función para búsqueda secuencial
    def busqueda_secuencial(df_left, col_left, df_right, cols_right, col_extra):
        df_left[col_extra] = np.nan

        for index, row in df_left.iterrows():
            valor = row[col_left]
            for col in cols_right:
                match = df_right[df_right[col] == valor]
                if not match.empty:
                    df_left.at[index, col_extra] = match.iloc[0][col_extra]
                    break  # Si encuentra, pasa a la siguiente fila
        return df_left

    # Aplicar la búsqueda secuencial
    df_palabras = busqueda_secuencial(
        df_palabras, 'Invoice', df_operaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'], 'Unnamed: 40'
    )

    # Aplicar búsqueda secuencial para df_facturas y df_operaciones
    df_facturas = busqueda_secuencial(
        df_facturas, 'Folio', df_operaciones, ['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA'], 'Unnamed: 40'
    )

    
    # Unir DATAFRAMES
    try:
        # FF CON F43
        df1_FF = pd.merge(df_facturas, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
        # FX CON F43
        df3_FX = pd.merge(df_palabras, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')

        # Concatenar resultados
        df_nacionales = pd.concat([df1_FF, df_facturas])
        df_extranjeros = pd.concat([df_operaciones, df3_FX])


        # Si df_unido_F está vacío, mostramos advertencia
        if df1_FF.empty:
            print("⚠️ Advertencia: No se encontraron coincidencias en df1_FF.")
        if df3_FX.empty:
            print("⚠️ Advertencia: No se encontraron coincidencias en df3_FX.")

    except Exception as e:
        print(f"Error with: {e}")

    # Guardar en Excel
    output_path = "./resources/files/datos_unidos.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        # Eliminar columnas no deseadas
        df_extranjeros = df_extranjeros.drop(columns=['Unnamed: 14', 'Unnamed: 25', 'CUSTODIA','Archivo', 'Denominacion cuenta contrapartida'])
        df_extranjeros_completas = df_extranjeros.dropna()

        df_nacionales = df_nacionales.drop(columns=['Denominacion cuenta contrapartida'])
        df_nacionales_completas = df_nacionales.dropna()

        #Guardar excel
        df_nacionales_completas.to_excel(writer, index=False, sheet_name="Nacionales")
        df_extranjeros_completas.to_excel(writer, index=False, sheet_name="Extranjeros")

buscar_columnas()