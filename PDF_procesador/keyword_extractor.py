import re

def extraer_valores(ruta_txt, palabras_clave):
    """Extrae el primer valor asociado a cada palabra clave desde un archivo de texto, validando que sea un número si es necesario."""
    try:
        with open(ruta_txt, 'r') as archivo:
            lineas = archivo.readlines()

        resultados = {}
        for palabra in palabras_clave:
            encontrado = False
            for linea in lineas:
                if palabra.lower() in linea.lower():
                    # Usar una expresión regular para capturar el texto después de la palabra clave hasta el primer espacio
                    patron = rf"{palabra}.*?[.:]?\s*(\S+)"
                    coincidencia = re.search(patron, linea, re.IGNORECASE)
                    if coincidencia:
                        valor = coincidencia.group(1).strip()
                        # Validar si el valor es un número entero
                        if palabra.lower() == "invoice":
                            resultados[palabra] = valor if valor.isdigit() else "False"
                        elif palabra.lower() in ["total", "currency", "amount due", "due", "total amount"]:
                            resultados[palabra] = valor.lstrip('$').strip()
                        else:
                            resultados[palabra] = valor
                        encontrado = True
                        break  # Detener búsqueda después de encontrar el primer resultado

            if not encontrado:
                resultados[palabra] = "False"  # No se encontró la palabra clave

        return resultados
    except Exception as e:
        print(f"Ocurrió un error al extraer valores: {e}")
        return {}

def verificar_palabras_clave(ruta_txt, palabras_verificar):
    """Verifica si las palabras clave específicas están presentes en el texto y devuelve un valor booleano."""
    try:
        with open(ruta_txt, 'r') as archivo:
            contenido = archivo.read()

        # Buscar cada palabra clave en el contenido del archivo
        resultados = {}
        for palabra in palabras_verificar:
            resultados[palabra] = palabra in contenido

        return resultados
    except Exception as e:
        print(f"Ocurrió un error al verificar palabras clave: {e}")
        return {}
