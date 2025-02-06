import re

def extraer_valores(ruta_txt, ruta_atributos, proveedor_encontrado, rango):
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
        

        # 🔹 Expresión regular mejorada para detectar el Total
        patron_total = re.compile(r"(?i)(Total Charges in USDs Due|Recibido Conforme Total|Total Amount|Amount Due)[^\d$]*([$]?\s*[\d,]+\.\d{2})")

        # 🔍 Buscar en todas las líneas sin depender de palabras clave
        for linea in lineas_txt:
            coincidencia_total = patron_total.search(linea)
            if coincidencia_total:
                print(f"🔍 Línea detectada con total: {linea.strip()}")  # DEPURACIÓN
                print(f"✅ Coincidencia extraída: {coincidencia_total.groups()}")  # DEPURACIÓN

                valor_total = coincidencia_total.group(2).replace(',', '').strip()
                resultados["Total"] = valor_total.lstrip('$')  # Remueve el signo de dólar si existe
                break  # No seguir buscando después de encontrar el total

        return resultados

    except Exception as e:
        print(f"Error al procesar {ruta_txt}: {e}")
        return {}
