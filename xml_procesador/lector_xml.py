import xmltodict
import os
from datetime import datetime

def leer_xml(ruta_xml):
    with open(ruta_xml, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    # Parsear XML a diccionario
    xml_dict = xmltodict.parse(xml_data)

    # Acceder a los nodos principales
    comprobante = xml_dict.get('cfdi:Comprobante', {})
    complemento = comprobante.get('cfdi:Complemento', {})
    emisor = comprobante.get('cfdi:Emisor', {})
    receptor = comprobante.get('cfdi:Receptor', {})
    impuestos = comprobante.get('cfdi:Impuestos', {})
    traslados = impuestos.get('cfdi:Traslados', {})

    # Obtener la tasa de IVA
    tasa_iva = 'N/A'
    if traslados:
        traslado = traslados.get('cfdi:Traslado', {})
        if isinstance(traslado, list):  # Si hay múltiples traslados
            for t in traslado:
                if t.get('@Impuesto') == '002':  # Filtra por IVA
                    tasa_iva = t.get('@TasaOCuota', 'N/A')
                    break
        elif isinstance(traslado, dict):  # Si hay un solo traslado
            if traslado.get('@Impuesto') == '002':
                tasa_iva = traslado.get('@TasaOCuota', 'N/A')

    # Obtener los conceptos
    conceptos = comprobante.get('cfdi:Conceptos', {}).get('cfdi:Concepto', [])
    if not isinstance(conceptos, list):  # Si hay un solo concepto, convertirlo en lista
        conceptos = [conceptos]

    # Obtener la primera ClaveProdServ de los conceptos
    clave_prod_serv = conceptos[0].get('@ClaveProdServ', 'N/A') if conceptos else 'N/A'

    # Obtener la Tasa o Cuota ISR (si existe)
    tasa_isr = 'N/A'
    for concepto in conceptos:
        impuestos_concepto = concepto.get('cfdi:Impuestos', {})
        retenciones = impuestos_concepto.get('cfdi:Retenciones', {})
        if retenciones:
            retencion = retenciones.get('cfdi:Retencion', {})
            if isinstance(retencion, list):  # Si hay múltiples retenciones
                for r in retencion:
                    if r.get('@Impuesto') == '001':  # Filtra por ISR
                        tasa_isr = r.get('@TasaOCuota', 'N/A')
                        break
            elif isinstance(retencion, dict):  # Si hay una sola retención
                if retencion.get('@Impuesto') == '001':
                    tasa_isr = retencion.get('@TasaOCuota', 'N/A')

    fecha = comprobante.get('@Fecha', 'N/A')[:10]
    if fecha != 'N/A':
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            fecha = 'N/A'           

    return {
        "Folio": comprobante.get('@Folio', 'N/A'),
        "Folio Fiscal": complemento.get('tfd:TimbreFiscalDigital', {}).get('@UUID', 'N/A'),
        "Fecha": fecha, 
        "ClaveProdServ": clave_prod_serv,
        "RFC_Receptor": receptor.get('@Rfc', 'N/A'),
        "RFC_Emisor": emisor.get('@Rfc', 'N/A'),
        "nombre_emisor": emisor.get('@Nombre', 'N/A'),
        "Moneda": comprobante.get('@Moneda', 'N/A'),
        "Metodo_Pago": comprobante.get('@MetodoPago', 'N/A'),
        "Tasa o Cuota IVA": tasa_iva,
        "Tasa o Cuota ISR": tasa_isr,
        "IVA": impuestos.get('@TotalImpuestosTrasladados', 'N/A'),
        "Retencion": impuestos.get('@TotalImpuestosRetenidos', 'N/A'),
        "Subtotal": comprobante.get('@SubTotal', 'N/A'),
        "Total": comprobante.get('@Total', 'N/A'),
    }

def asignar_ids(archivos_xml):
    # Diccionario para almacenar el ID de cada carpeta
    carpetas_ids = {}
    id_actual = 0  # Contador para IDs incrementales

    datos_facturas = []
    for ruta_xml in archivos_xml:
        # Obtener el nombre de la carpeta que contiene el archivo XML
        carpeta = os.path.basename(os.path.dirname(ruta_xml))

        # Si la carpeta no está en el diccionario, asignarle un nuevo ID
        if carpeta not in carpetas_ids:
            id_actual += 1
            carpetas_ids[carpeta] = id_actual

        try:
            # Leer el archivo XML
            factura = leer_xml(ruta_xml)
            # Asignar el ID de la carpeta al campo "ID" de la factura
            factura["ID"] = carpetas_ids[carpeta]
            datos_facturas.append(factura)
        except Exception as e:
            print(f"Error al procesar el archivo {ruta_xml}: {e}")

        if factura:
            factura["Archivo"] = os.path.basename(ruta_xml)
            datos_facturas.append(factura)
    return datos_facturas