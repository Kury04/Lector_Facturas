import pdfplumber
import glob
import os
import re


def buscar_pdfs_en_carpeta(carpeta):
    """Busca todos los archivos PDF en una carpeta y subcarpetas."""
    archivos_pdf = glob.glob(f"{carpeta}/**/*.pdf", recursive=True)
    if not archivos_pdf:
        print(f"No se encontraron archivos PDF en {carpeta}")
    else:
        print(f"Se encontraron {len(archivos_pdf)} archivos PDF.")
    return archivos_pdf


def consolidar_lineas(texto):
    """Consolida líneas consecutivas en una sola línea."""
    lineas = texto.splitlines()
    lineas_consolidadas = [
        lineas[i] + " " + lineas[i + 1] if i + 1 < len(lineas) else lineas[i]
        for i in range(0, len(lineas), 2)
    ]
    return "\n".join(lineas_consolidadas)


def extraer_texto_pdf(ruta_pdf, ruta_txt):
    """Extrae texto de un archivo PDF y lo guarda en un archivo TXT."""
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            texto = ""
            for page in pdf.pages:
                texto += page.extract_text()
            texto_consolidado = consolidar_lineas(texto)

        with open(ruta_txt, 'w') as archivo_txt:
            archivo_txt.write(texto_consolidado)

        print(f"Texto extraído y guardado en {ruta_txt}.")
        return True
    except Exception as e:
        print(f"Error al procesar {ruta_pdf}: {e}")
        return False


def extraer_valores_desde_txt(ruta_txt, palabras_clave):
    """Extrae el primer valor asociado a cada palabra clave desde un archivo TXT."""
    try:
        with open(ruta_txt, 'r') as archivo:
            lineas = archivo.readlines()

        resultados = {}
        for palabra in palabras_clave:
            for linea in lineas:
                if palabra.lower() in linea.lower():
                    # Usar una expresión regular para capturar el texto después de la palabra clave
                    patron = rf"{palabra}.*?:\s*(.+)"
                    coincidencia = re.search(patron, linea, re.IGNORECASE)
                    if coincidencia:
                        resultados[palabra] = coincidencia.group(1).strip()
                        break  # Detener búsqueda después de encontrar el primer resultado
        return resultados

    except Exception as e:
        print(f"Error al procesar {ruta_txt}: {e}")
        return {}


def procesar_pdfs(carpeta, palabras_clave):
    """Procesa todos los PDFs en una carpeta y extrae valores de interés."""
    archivos_pdf = buscar_pdfs_en_carpeta(carpeta)

    if not archivos_pdf:
        return

    for ruta_pdf in archivos_pdf:
        nombre_txt = os.path.basename(ruta_pdf).replace('.pdf', '.txt')
        ruta_txt = os.path.join(carpeta, nombre_txt)

        # Extraer texto del PDF y guardarlo en un archivo TXT
        if extraer_texto_pdf(ruta_pdf, ruta_txt):
            # Buscar palabras clave en el archivo TXT
            resultados = extraer_valores_desde_txt(ruta_txt, palabras_clave)
            
            # Imprimir resultados
            print(f"\nResultados para {os.path.basename(ruta_pdf)}:")
            for palabra, valor in resultados.items():
                print(f"  {palabra}: {valor}")

            # Eliminar el archivo TXT después de procesarlo
            try:
                os.remove(ruta_txt)
                print(f"Archivo temporal {ruta_txt} eliminado.")
            except Exception as e:
                print(f"No se pudo eliminar {ruta_txt}: {e}")


# Configuración de rutas y palabras clave
carpeta = 'C:/Users/jparedes_consultant/Documents/Alfaparf PYTHON/Lector_Facturas/files/FX'
palabras_clave = ['Tax ID', 'Invoice', 'Invoice Date', 'Total', 'Currency']

# Ejecutar el procesamiento
procesar_pdfs(carpeta, palabras_clave)

