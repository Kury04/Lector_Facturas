from PDF_procesador.file_utils import buscar_pdfs_en_carpeta
from PDF_procesador.pdf_utils import extraer_texto_pdf
from PDF_procesador.keyword_extractor import extraer_valores, verificar_palabras_clave
from xml_procesador.procesador import procesar_cfdis
from xml_procesador.exportar_excel import crear_excel
from utils.archivos import leer_archivo
import os

# Configuración de rutas
carpeta = input("Inserta la ruta plis: ")
ruta_atributos = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/Lector_Facturas-main/resources/atributos.txt"
archivo_proveedores = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/Lector_Facturas-main/resources/proveedores_extranjeros.txt"
ruta_excel = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/Lector_Facturas-main/resources/files/prueba_excel.xlsx"

# Leer palabras clave y proveedores extranjeros
palabras_clave = leer_archivo(ruta_atributos)
proveedores = leer_archivo(archivo_proveedores)

# Inicializar listas para almacenar los datos
datos_facturas = procesar_cfdis(carpeta)
datos_palabras = []

# Procesar archivos en la carpeta
if palabras_clave:
    archivos_en_carpeta = os.listdir(carpeta)
    
    # Buscar y procesar archivos PDF
    archivos_pdf = buscar_pdfs_en_carpeta(carpeta)
    for ruta_pdf in archivos_pdf:
        nombre_txt = os.path.basename(ruta_pdf).replace('.pdf', '.txt')
        ruta_txt = os.path.join(carpeta, nombre_txt)

        # Extraer texto del PDF y guardarlo en un archivo TXT
        texto_pdf = extraer_texto_pdf(ruta_pdf, ruta_txt)
        if texto_pdf:
            print(f"Archivo PDF convertido a TXT: {ruta_txt}")

            # Leer el archivo TXT
            with open(ruta_txt, 'r') as archivo_txt:
                texto_txt = archivo_txt.read()

            # Validar si el archivo TXT contiene algún proveedor extranjero
            proveedor_encontrado = any(proveedor in texto_txt for proveedor in proveedores)
            
            # Eliminar el archivo TXT si no contiene un proveedor extranjero
            if not proveedor_encontrado:
                os.remove(ruta_txt)
                print(f"El archivo TXT {ruta_txt} ha sido eliminado porque no contiene proveedores extranjeros")
            else:
                # Buscar palabras clave en el archivo TXT
                resultados = extraer_valores(ruta_txt, palabras_clave)
                resultados["Archivo"] = os.path.basename(ruta_txt)  # Agregar el nombre del archivo
                datos_palabras.append(resultados)  # Guardar en la lista acumulativa

                # Verificar palabras clave específicas
                palabras_verificar = ["USD", "DOB001109DK5"]
                booleans = verificar_palabras_clave(ruta_txt, palabras_verificar)
                print(f"Resultados para {os.path.basename(ruta_pdf)}:")
                for palabra, encontrado in booleans.items():
                    print(f"  {palabra}: {True if encontrado else False}")

# Exportar a Excel si hay datos
if datos_facturas or datos_palabras:
    crear_excel(datos_facturas, datos_palabras, ruta_excel)
    print(f"Excel exportado en {ruta_excel}")
else:
    print("No hay datos para exportar.")