import glob
import os

def buscar_pdfs_en_carpeta(carpeta):
    """Busca todos los archivos PDF en una carpeta y subcarpetas."""
    archivos_pdf = glob.glob(f"{carpeta}/**/*.pdf", recursive=True)
    if not archivos_pdf:
        print(f"No se encontraron archivos PDF en {carpeta}")
    else:
        print(f"Se encontraron {len(archivos_pdf)} archivos PDF.")
    return archivos_pdf