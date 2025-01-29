import pdfplumber
import PyPDF2
import os

def consolidar_lineas(texto):
    """Consolida líneas consecutivas en una sola línea."""
    lineas = texto.splitlines()
    lineas_consolidadas = [
        lineas[i] + " " + lineas[i + 1] if i + 1 < len(lineas) else lineas[i]
        for i in range(0, len(lineas), 2)
    ]
    return "\n".join(lineas_consolidadas)

def extraer_texto_pdf(ruta_pdf, ruta_txt):
    """Extrae texto de un archivo PDF usando pdfplumber, con PyPDF2 como respaldo."""
    try:
        # Intentar usar pdfplumber para extraer texto
        with pdfplumber.open(ruta_pdf) as pdf:
            texto = ""
            for pagina in pdf.pages:
                texto += pagina.extract_text()
            texto_consolidado = consolidar_lineas(texto)

        # Si pdfplumber tiene éxito
        with open(ruta_txt, 'w') as archivo_txt:
            archivo_txt.write(texto_consolidado)

        print(f"Texto extraído y guardado en {ruta_txt}.")
        return texto_consolidado

    except Exception as e_pdfplumber:
        print(f"Error al procesar con pdfplumber {ruta_pdf}: {e_pdfplumber}")

        # Como respaldo, intentar usar PyPDF2
        try:
            with open(ruta_pdf, 'rb') as archivo_pdf:
                lector = PyPDF2.PdfReader(archivo_pdf)
                texto = ""
                for pagina in lector.pages:
                    texto += pagina.extract_text()

            with open(ruta_txt, 'w') as archivo_txt:
                archivo_txt.write(texto)

            print(f"Texto extraído y guardado en {ruta_txt}.")
            return texto
        except Exception as e_pypdf2:
            print(f"Error al procesar con PyPDF2 {ruta_pdf}: {e_pypdf2}")
            return None
