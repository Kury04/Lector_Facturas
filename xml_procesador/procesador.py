import os
import glob
from tkinter import messagebox
from .lector_xml import leer_xml, asignar_ids
from PDF_procesador.file_utils import buscar_pdfs_en_carpeta
from PDF_procesador.pdf_utils import extraer_texto_pdf
from PDF_procesador.keyword_extractor import extraer_valores
from xml_procesador.exportar_excel import crear_excel
from utils.archivos import leer_archivo

def procesar_documentos(carpeta, progress_bar):
    ruta_atributos = "resources/atributos.txt"
    archivo_proveedores = "resources/proveedores_extranjeros.txt"
    ruta_excel = os.path.join(carpeta, "Datos Facturas.xlsx")

    palabras_clave = leer_archivo(ruta_atributos)
    proveedores = leer_archivo(archivo_proveedores)

    # Procesar archivos XML
    archivos_xml = glob.glob(f"{carpeta}/**/*.xml", recursive=True)
    datos_facturas = asignar_ids(archivos_xml) if archivos_xml else []
    for ruta_xml in archivos_xml:
        print(f"Procesando archivo: {ruta_xml}")
        try:
            factura = leer_xml(ruta_xml)
            datos_facturas.append(factura)
        except Exception as e:
            print(f"Error al procesar el archivo {ruta_xml}: {e}")

    datos_palabras = []
    

    # Procesar archivos PDF si hay palabras clave
    if palabras_clave:
        archivos_pdf = buscar_pdfs_en_carpeta(carpeta)
        total_archivos = len(archivos_pdf)

        for i, ruta_pdf in enumerate(archivos_pdf, 1):
            nombre_txt = os.path.basename(ruta_pdf).replace('.pdf', '.txt')
            ruta_txt = os.path.join(carpeta, nombre_txt)

            texto_pdf = extraer_texto_pdf(ruta_pdf, ruta_txt)
            if texto_pdf:
                with open(ruta_txt, 'r') as archivo_txt:
                    texto_txt = archivo_txt.read()

                for proveedor in proveedores:
                    if proveedor in texto_txt:
                        rangos = {
                            "C.H. Robinson": (1, 5),
                            "SOLUTRANS LOGISTICS S,A": (7, 11),
                            "SAMSUNG SDS AMERICA, INC.": (13, 16),
                            "Transplace Mexico LLC": (18, 22)
                        }

                        if proveedor in rangos:
                            resultados = extraer_valores(ruta_txt, ruta_atributos, proveedor, rango=rangos[proveedor])
                            if resultados:
                                resultados["Archivo"] = os.path.basename(ruta_txt)
                                datos_palabras.append(resultados)
                        break

            progress_bar.set(i / total_archivos)

        # Eliminar archivos temporales .txt
        for ruta_txt in [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith('.txt')]:
            os.remove(ruta_txt)
        
    # Exportar resultados a Excel
    if datos_facturas or datos_palabras:
        crear_excel(datos_facturas, datos_palabras, ruta_excel)
        messagebox.showinfo("Éxito", f"Datos exportados a {ruta_excel}")
    else:
        messagebox.showwarning("Atención", "No se encontraron datos para exportar.")
