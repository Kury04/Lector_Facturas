import re
from datetime import datetime

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
            "nombre_emisor": proveedor_encontrado,
            "TAX ID": "N/A",
            "Invoice": "Error[Invoice]",
            "Fecha": "Error[Fecha]",
            "Moneda": "USD",
            "Total": "Error[Total]",
            "RFC_Receptor": "DOB001109DK5"
        }

        # Mapeo de palabras clave
        mapeo_palabras = {
            "TAX ID": ["tax id", "cedula juridica"],
            "Invoice": ["invoice", "invoice no", "invoice number", "numero interno"],
            "Fecha": ["date", "fecha", "invoice date", "due date"],
            "Moneda": ["moneda", "currency"]
        }

        # Expresión regular para extraer el "Total" (segundo código)
        patron_total = re.compile(r"(?i)(Total Charges in USDs Due|Recibido Conforme Total|Total Amount|Amount Due)[^\d$]*([$]?\s*[\d,]+\.\d{2})")

        # Buscar en todas las líneas el "Total"
        for linea in lineas_txt:
            coincidencia_total = patron_total.search(linea)
            if coincidencia_total:
                valor_total = coincidencia_total.group(2).replace(',', '').strip()
                resultados["Total"] = valor_total.lstrip('$')  # Remueve el signo de dólar si existe
                break  # No seguir buscando después de encontrar el total

        # Buscar otros valores según palabras clave (primer código)
        for palabra in palabras_clave:
            for linea in lineas_txt:
                if palabra.lower() in linea.lower():
                    # Si el proveedor es C.H. Robinson y la palabra clave es "Fecha", usar un formato especial
                    if proveedor_encontrado == "C.H. Robinson Company, Inc" and palabra.lower() in ["date", "fecha", "invoice date", "due date"]:
                        patron_fecha = re.compile(r"(?i)Invoice Date:\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})")
                        coincidencia_fecha = patron_fecha.search(linea)
                        if coincidencia_fecha:
                            fecha_str = coincidencia_fecha.group(1)
                            # Convertir la fecha al formato deseado (00/00/0000)
                            fecha_obj = datetime.strptime(fecha_str, "%B %d, %Y")
                            resultados["Fecha"] = fecha_obj.strftime("%d/%m/%Y")
                            break  # Salir del bucle si se encuentra la fecha
                    else:
                        # Para otros proveedores o campos, usar la lógica original
                        patron = rf"{palabra}.*?[.:$]?\s*(\S+)"
                        coincidencia = re.search(patron, linea, re.IGNORECASE)
                        if coincidencia:
                            valor = coincidencia.group(1).strip()
                            for columna, palabras in mapeo_palabras.items():
                                if palabra.lower() in palabras:
                                    resultados[columna] = valor
                                    break  # Se encontró el valor, no seguir buscando
                            break  # Pasar a la siguiente palabra clave

        return resultados

    except Exception as e:
        print(f"Error al procesar {ruta_txt}: {e}")
        return {}