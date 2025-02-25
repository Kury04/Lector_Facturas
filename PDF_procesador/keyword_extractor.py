import re
import os
import sys
from datetime import datetime

# Diccionario global para almacenar IDs por carpeta
carpetas_ids = {}
id_actual = 0  # Contador incremental para IDs


def asignar_id(ruta_txt):
    """Asigna un ID único basado en la carpeta del archivo TXT."""
    global id_actual  # Usamos la variable global para mantener el conteo
    carpeta = os.path.basename(os.path.dirname(ruta_txt))  # Obtiene el nombre de la carpeta

    if carpeta not in carpetas_ids:
        id_actual += 1  # Incrementa el ID solo si la carpeta no tiene uno asignado
        carpetas_ids[carpeta] = id_actual

    return carpetas_ids[carpeta]  # Retorna el ID asignado a la carpeta


def extraer_valores(ruta_txt, ruta_atributos, proveedor_encontrado, rango):
    """Extrae valores clave de un archivo TXT y asigna un ID basado en su carpeta."""
    try:
        id_factura = asignar_id(ruta_txt)  # Asignar ID a la factura

        with open(ruta_txt, 'r') as archivo:
            lineas_txt = archivo.readlines()

        with open(ruta_atributos, 'r') as archivo_atributos:
            palabras_clave = [linea.strip() for i, linea in enumerate(archivo_atributos) if rango[0] <= i + 1 <= rango[1]]

        if not proveedor_encontrado:
            return {}  # No se extraen datos sin proveedor identificado

        resultados = {
            "ID": id_factura,  # ID asignado por carpeta
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

        # Expresión regular para extraer el "Total"
        patron_total = re.compile(r"(?i)(Total Charges in USDs Due|Recibido Conforme Total|Total Amount|Amount Due)[^\d$]*([$]?\s*[\d,]+\.\d{2})")

        # Buscar "Total"
        for linea in lineas_txt:
            coincidencia_total = patron_total.search(linea)
            if coincidencia_total:
                valor_total = coincidencia_total.group(2).replace(',', '').strip()
                resultados["Total"] = valor_total.lstrip('$')
                break

        # Buscar otros valores según palabras clave
        for palabra in palabras_clave:
            for linea in lineas_txt:
                if palabra.lower() in linea.lower():
                    if proveedor_encontrado == "C.H. Robinson Company, Inc" and palabra.lower() in ["date", "fecha", "invoice date", "due date"]:
                        patron_fecha = re.compile(r"(?i)Invoice Date:\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})")
                        coincidencia_fecha = patron_fecha.search(linea)
                        if coincidencia_fecha:
                            fecha_str = coincidencia_fecha.group(1)
                            fecha_obj = datetime.strptime(fecha_str, "%B %d, %Y")
                            resultados["Fecha"] = fecha_obj.strftime("%d/%m/%Y")
                            break
                    else:
                        patron = rf"{palabra}.*?[.:$]?\s*(\S+)"
                        coincidencia = re.search(patron, linea, re.IGNORECASE)
                        if coincidencia:
                            valor = coincidencia.group(1).strip()
                            for columna, palabras in mapeo_palabras.items():
                                if palabra.lower() in palabras:
                                    resultados[columna] = valor
                                    break
                            break

        return resultados

    except Exception as e:
        print(f"Error al procesar {ruta_txt}: {e}")
        return {}
