import xmltodict

def leer_xml(ruta_xml):
    with open(ruta_xml, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    # Parsear XML a diccionario
    xml_dict = xmltodict.parse(xml_data)

    comprobante = xml_dict.get('cfdi:Comprobante', {})
    complemento = comprobante.get('cfdi:Complemento', {})
    emisor = comprobante.get('cfdi:Emisor', {})
    impuestos = comprobante.get('cfdi:Impuestos', {})

    return {
        "folio": comprobante.get('@Folio', 'N/A'),
        "fecha": comprobante.get('@Fecha', 'N/A')[:10],
        "moneda": comprobante.get('@Moneda', 'N/A'),
        "metodo_pago": comprobante.get('@MetodoPago', 'N/A'),
        "subtotal": comprobante.get('@SubTotal', 'N/A'),
        "total": comprobante.get('@Total', 'N/A'),
        "rfc_emisor": emisor.get('@Rfc', 'N/A'),
        "nombre_emisor": emisor.get('@Nombre', 'N/A'),
        "total_impuestos": impuestos.get('@TotalImpuestosTrasladados', 'N/A'),
        "uuid": complemento.get('tfd:TimbreFiscalDigital', {}).get('@UUID', 'N/A'),
    }
