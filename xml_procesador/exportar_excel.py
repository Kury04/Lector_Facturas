import pandas as pd

def crear_excel(datos_facturas, datos_palabras, ruta_excel):
    """
    Crea un archivo Excel con dos hojas: 
    - "Datos Facturas" para los datos extraídos de los XML.
    - "Palabras Clave" para los valores encontrados en los archivos TXT.
    
    :param datos_facturas: Lista de diccionarios con datos de facturas extraídas de XML.
    :param datos_palabras: Lista de diccionarios con palabras clave encontradas en TXT.
    :param ruta_excel: Ruta donde se guardará el archivo Excel.
    """
    try:
        # Verificar si hay datos para exportar
        if not datos_facturas and not datos_palabras:
            print("No hay datos para exportar.")
            return

        # Crear un archivo Excel con pandas
        with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
            # Hoja 1: Datos de Facturas XML
            if datos_facturas:
                df_facturas = pd.DataFrame(datos_facturas)
                df_facturas.to_excel(writer, sheet_name="Datos Facturas", index=False)
            
            # Hoja 2: Palabras Clave en TXT
            if datos_palabras:
                df_palabras = pd.DataFrame(datos_palabras)
                df_palabras.to_excel(writer, sheet_name="Palabras Clave", index=False)

        print(f"Datos exportados correctamente a {ruta_excel}")

    except Exception as e:
        print(f"Error al exportar a Excel: {e}")