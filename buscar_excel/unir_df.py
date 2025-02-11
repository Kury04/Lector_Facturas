import pandas as pd
import os
from columns_extractor import extraer_columnas
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from xml_procesador.procesador import procesar_documentos

def buscar_columnas():
    df_f43, _= extraer_columnas()

    # Procesar los documentos en la carpeta especificada
    carpeta = "./resources/files"
    _, df_palabras = procesar_documentos(carpeta)
    df_facturas, _ = procesar_documentos(carpeta)

    # Normalizar claves de unión
    df_f43["Denominacion cuenta contrapartida"] = df_f43["Denominacion cuenta contrapartida"].str.strip().str.upper()
    df_facturas["nombre_emisor"] = df_facturas["nombre_emisor"].str.strip().str.upper()
    df_palabras["nombre_emisor"] = df_palabras["nombre_emisor"].str.strip().str.upper()

    # # Depurar claves antes de hacer merge
    # print("Valores únicos en df_f43:", df_f43["Denominacion cuenta contrapartida"].unique())
    # print("Valores únicos en df_facturas:", df_facturas["nombre_emisor"].unique())
    # print("Valores únicos en df_palabras:", df_palabras["nombre_emisor"].unique())

    # Unir DATAFRAMES
    try:
        #FX CON F43
        df1_FF_F43 = pd.merge(df_facturas, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')

        #FF CON F43
        df2_FX_F43 = pd.merge(df_palabras, df_f43, how='outer', left_on='nombre_emisor', right_on='Denominacion cuenta contrapartida')

        # Si df_unido_F está vacío, mostramos advertencia
        if df1_FF_F43.empty:
            print("⚠️ Advertencia: No se encontraron coincidencias en df_facturas y df_palabras.")

        elif df2_FX_F43.empty:
            print("⚠️ Advertencia: No se encontraron coincidencias en df_facturas y df_palabras.")

    except Exception as e:
        print(f"Error with: {e}")

    print(f"Esto son los xml{df_facturas}")
    # # Unir con F-43
    # df_unido = pd.merge(df_f43, df_unido_F, how='inner', left_on='Denominacion cuenta contrapartida', right_on='nombre_emisor')

    # # Si df_unido está vacío, mostramos advertencia
    # if df_unido.empty:
    #     print("⚠️ Advertencia: No se encontraron coincidencias en df_f43 y df_unido_F.")

    output_path = "./resources/files/datos_unidos.xlsx"

    # Guardar en Excel
    df2_FX_F43.to_excel(output_path, index=False, sheet_name="Datos_Procesados")

    print(f"Datos exportados a {output_path}")
    print(f"Dataframe unido de ff y f43 {df1_FF_F43}")
    print(f"Dataframe unido de ff y f43 {df2_FX_F43}")

buscar_columnas()
