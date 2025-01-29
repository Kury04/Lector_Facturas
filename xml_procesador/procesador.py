from .lector_xml import leer_xml
from .exportar_excel import crear_excel
import glob
import os

def procesar_cfdis(carpeta):
    # Buscar archivos XML
    archivos_xml = glob.glob(f"{carpeta}/**/*.xml", recursive=True)
    
    if not archivos_xml:
        print(f"No se encontraron archivos XML en la carpeta: {carpeta}")
        return []  # Retorna lista vacía si no hay archivos

    datos_facturas = []

    for ruta_xml in archivos_xml:
        print(f"Procesando archivo: {ruta_xml}")
        try:
            factura = leer_xml(ruta_xml)
            datos_facturas.append(factura)
        except Exception as e:
            print(f"Error al procesar el archivo {ruta_xml}: {e}")

    return datos_facturas  # Retorna la lista de datos procesados

# # Ejecutar la función y usar el resultado
# carpeta = "ruta/de/tu/carpeta"
# ruta_excel = "ruta/del/archivo.xlsx"

# datos_facturas = procesar_cfdis(carpeta)  # Llamamos a la función y guardamos el resultado
# if datos_facturas:  # Si hay datos, los exportamos
#     crear_excel(datos_facturas, ruta_excel)
#     print(f"Datos exportados exitosamente a {ruta_excel}")
# else:
#     print("No hay datos para exportar.")
