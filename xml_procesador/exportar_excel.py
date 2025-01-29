import openpyxl

def crear_excel(datos_facturas, ruta_excel):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos Facturas"

    # Encabezados
    headers = [
        "Folio", "Rfc Emisor", "Emisor", "Fecha", "Metodo Pago", 
        "Moneda", "Subtotal", "IVA", "Total", "Fol Fiscal"
    ]
    ws.append(headers)

    # Escribir datos
    for factura in datos_facturas:
        ws.append([
            factura["folio"], factura["rfc_emisor"], factura["nombre_emisor"],
            factura["fecha"], factura["metodo_pago"], factura["moneda"],
            factura["subtotal"], factura["total_impuestos"],
            factura["total"], factura["uuid"]
        ])

    wb.save(ruta_excel)
