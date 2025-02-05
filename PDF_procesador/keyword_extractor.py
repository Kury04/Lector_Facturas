import re
import os

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
            "TAX ID": "N/A",
            "Invoice": "Error[Invoice]",
            "Fecha": "Error[Fecha]",
            "Moneda": "USD",
            "Total": "Error[Total]"
        }

        # Definir reglas para cada campo
        mapeo_palabras = {
            "TAX ID": ["tax id", "cedula juridica"],
            "Invoice": ["invoice", "invoice no", "invoice number", "numero interno"],
            "Fecha": ["date", "fecha", "invoice date", "due date"],
            "Moneda": ["moneda", "currency"],
            "Total": ["due", "Recibido Conforme total", "total amount", "amount due"]
        }



        for palabra in palabras_clave:
            encontrado = False  # Inicializar antes del loop

            for linea in lineas_txt:
                if palabra.lower() in linea.lower():
                    patron = rf"{palabra}.*?[.:$]?\s*(\S+)"
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
                        elif palabra.lower() in ["Recibido Conforme Total", "Amount due", "Due", "Total Amount"]:
                            valor_limpio = valor.lstrip('$').strip()
                            try:
                                float(valor_limpio)  # Intenta convertir a float
                                resultados[palabra] = valor_limpio
                            except ValueError:
                                resultados[palabra] = "False"
                        else:
                            resultados[palabra] = valor
                        encontrado = True
                        break
        return resultados
    #Como hago para que si encuentra la primera coincidencia y es false pase a la que sigue hasta que encuentre con un valor

    except Exception as e:
        print(f"Error al procesar {ruta_txt}: {e}")
        return {}



def verificar_palabras_clave(ruta_txt, ruta_pdf, palabras_verificar):
    """Verifica si las palabras clave específicas están presentes en el texto."""
    try:
        with open(ruta_txt, 'r') as archivo:
            contenido = archivo.read()

        #Verificar palabras clave
        palabras_verificar = ["USD", "DOB001109DK5"]
        booleans = verificar_palabras_clave(ruta_txt, palabras_verificar)
        print(f"Resultados de verificación para {os.path.basename(ruta_pdf)}:")
        for palabra, encontrado in booleans.items():
            print(f"  {palabra}: {True if encontrado else False}")

        resultados = {palabra: palabra in contenido for palabra in palabras_verificar}
        return resultados
    except Exception as e:
        print(f"Error al verificar palabras clave: {e}")
        return {}