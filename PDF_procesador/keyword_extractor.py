import re

def extraer_valores(ruta_txt, ruta_atributos, proveedor_encontrado, rango=(3, 6)):
    """Extrae valores clave de un archivo TXT según el proveedor y el rango asignado en atributos.txt."""
    try:
        with open(ruta_txt, 'r') as archivo:
            lineas_txt = archivo.readlines()

        # Leer palabras clave dentro del rango indicado
        with open(ruta_atributos, 'r') as archivo_atributos:
            palabras_clave = [linea.strip() for i, linea in enumerate(archivo_atributos) if rango[0] <= i + 1 <= rango[1]]

        if not proveedor_encontrado:
            return {}  # No se extraen datos si no hay proveedor identificado

        resultados = {
            "Nombre proveedor": proveedor_encontrado,
            "TAX ID": "False",
            "Invoice": "False",
            "Fecha": "False",
            "Moneda": "False",
            "Total": "False"
        }

        # Definir reglas para cada campo
        mapeo_palabras = {
            "TAX ID": ["tax id", "cedula juridica"],
            "Invoice": ["invoice", "invoice no", "invoice number", "numero interno"],
            "Fecha": ["date", "fecha", "invoice date"],
            "Moneda": ["moneda", "currency", "usd"],
            "Total": ["due", "total", "total amount", "amount due"]
        }

        for palabra in palabras_clave:
            encontrado = False  # Inicializar antes del loop

            for linea in lineas_txt:
                if palabra.lower() in linea.lower():
                    patron = rf"{palabra}.*?[.:]?\s*(\S+)"
                    coincidencia = re.search(patron, linea, re.IGNORECASE)
                    if coincidencia:
                        valor = coincidencia.group(1).strip()

                        for columna, palabras in mapeo_palabras.items():
                            if palabra.lower() in palabras:
                                if columna == "Moneda" and "usd" in valor.lower():
                                    resultados[columna] = "USD"
                                else:
                                    resultados[columna] = valor
                                break  # Salir después de encontrar la coincidencia

                        # Validar si el valor es un número entero o un monto
                        if palabra.lower() == "invoice":
                            resultados[palabra] = valor if valor.isdigit() else "False"
                        elif palabra.lower() in ["total", "currency", "amount due", "due", "total amount"]:
                            valor_limpio = valor.lstrip('$').strip()
                            try:
                                float(valor_limpio)
                                resultados[palabra] = valor_limpio
                            except ValueError:
                                resultados[palabra] = "False"
                        else:
                            resultados[palabra] = valor

                        encontrado = True  # Se encontró al menos una coincidencia
                        break  # Solo toma la primera coincidencia

            if not encontrado:
                resultados[palabra] = "False"

        return resultados
    except Exception as e:
        print(f"Error al procesar {ruta_txt}: {e}")
        return {}



def verificar_palabras_clave(ruta_txt, palabras_verificar):
    """Verifica si las palabras clave específicas están presentes en el texto."""
    try:
        with open(ruta_txt, 'r') as archivo:
            contenido = archivo.read()

        resultados = {palabra: palabra in contenido for palabra in palabras_verificar}
        return resultados
    except Exception as e:
        print(f"Error al verificar palabras clave: {e}")
        return {}
