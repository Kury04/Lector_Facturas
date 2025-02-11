import pandas as pd
import os
from columns_extractor import extraer_columnas
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from xml_procesador.procesador import procesar_documentos

def buscar_columnas():

    # Procesar los documentos en la carpeta especificada
    carpeta = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/Sarita XML/EXPORTACIÓN/1. ENERO"

    # DATAFRAMES
    _, df_palabras = procesar_documentos(carpeta)
    df_facturas, _ = procesar_documentos(carpeta)
    df_f43, _= extraer_columnas()
    _, df_operaciones = extraer_columnas()

    # Normalizar claves de unión
    df_f43["Denominacion cuenta contrapartida"] = df_f43["Denominacion cuenta contrapartida"].str.strip().str.upper()
    df_facturas["nombre_emisor"] = df_facturas["nombre_emisor"].str.strip().str.upper()
    df_palabras["nombre_emisor"] = df_palabras["nombre_emisor"].str.strip().str.upper()
    df_facturas["Folio"] = df_facturas["Folio"].str.strip().str.upper()

    # # Depurar claves antes de hacer merge
    # print("Valores únicos en df_f43:", df_f43["Denominacion cuenta contrapartida"].unique())
    # print("Valores únicos en df_facturas:", df_facturas["nombre_emisor"].unique())
    # print("Valores únicos en df_palabras:", df_palabras["nombre_emisor"].unique())
    print(df_facturas["Folio"].unique())
    # print(df_operaciones["Unnamed: 14"].unique())


    # Unir DATAFRAMES
    try:
        #FF CON F43
        df1_FF = pd.merge(df_facturas, df_f43, how='right', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
        #FF CON OPERACIONES
        df2_FF = pd.merge(df_facturas,df_operaciones, how='outer', left_on='Folio', right_on='Unnamed: 25')
        #FX CON F43
        df3_FX = pd.merge(df_palabras, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')
        #FX CON operaciones
        df4_FX = pd.merge(df_palabras,df_operaciones, how='outer', left_on='Invoice', right_on='Unnamed: 25')

        df_absoluto = pd.concat([df1_FF,df2_FF,df3_FX,df4_FX])
        df_nacionales = pd.concat([df1_FF,df2_FF])
        # Si df_unido_F está vacío, mostramos advertencia
        if df1_FF.empty:
            print("⚠️ Advertencia: No se encontraron coincidencias en df_facturas y df_palabras.")
        if df2_FF.empty:
            print("⚠️ Advertencia: No se encontraron coincidencias en df_facturas y df_palabras.")
        if df3_FX.empty:
            print("⚠️ Advertencia: No se encontraron coincidencias en df_facturas y df_palabras.")

    except Exception as e:
        print(f"Error with: {e}")

    print(f"Esto son los xml{df_absoluto}")
    # # Unir con F-43
    # df_unido = pd.merge(df_f43, df_unido_F, how='inner', left_on='Denominacion cuenta contrapartida', right_on='nombre_emisor')

    # # Si df_unido está vacío, mostramos advertencia
    # if df_unido.empty:
    #     print("⚠️ Advertencia: No se encontraron coincidencias en df_f43 y df_unido_F.")

    output_path = "./resources/files/datos_unidos.xlsx"

    # Guardar en Excel
    df_nacionales.to_excel(output_path, index=False, sheet_name="Datos_Procesados")

    # print(f"Datos exportados a {output_path}")
    # print(f"Dataframe unido de ff y f43 {df1_FF}")
    # print(f"Dataframe unido de ff y f43 {df4_FX}")

buscar_columnas()
