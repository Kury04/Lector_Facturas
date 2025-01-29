from .lector_xml import leer_xml
import glob
import os

def procesar_cfdis(carpeta):
    # Buscar archivos XML
    archivos_xml = glob.glob(f"{carpeta}/**/*.xml", recursive=True)
    
    if not archivos_xml:
        print(f"No se encontraron archivos XML en la carpeta: {carpeta}")
        return []

    datos_facturas = []

    for ruta_xml in archivos_xml:
        print(f"Procesando archivo: {ruta_xml}")
        try:
            factura = leer_xml(ruta_xml)
            datos_facturas.append(factura)
        except Exception as e:
            print(f"Error al procesar el archivo {ruta_xml}: {e}")

    return datos_facturas  # Retorna la lista de datos procesados

