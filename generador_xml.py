from xml_procesador.procesador import procesar_cfdis
from xml_procesador.exportar_excel import crear_excel

import os

# Configuración de rutas
carpeta = input("Inserta la ruta plis: ")
ruta_atributos = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/Lector_Facturas-main/resources/atributos.txt"
archivo_proveedores = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/Lector_Facturas-main/resources/proveedores_extranjeros.txt"
ruta_excel = "C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/Lector_Facturas-main/resources/files/Datos_XML.xlsx"


# Inicializar listas para almacenar los datos
datos_facturas = procesar_cfdis(carpeta)

# Exportar a Excel si hay datos
if datos_facturas:
    crear_excel(datos_facturas, ruta_excel)
    print(f"Excel exportado en {ruta_excel}")
else:
    print("No hay datos para exportar.")