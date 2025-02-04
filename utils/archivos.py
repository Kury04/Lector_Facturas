def leer_archivo(ruta):
    try:
        with open(ruta, 'r') as archivo:
            contenido = [line.strip() for line in archivo.readlines()]
        print(f"Se cargaron {len(contenido)} elementos desde {ruta}.")
        return contenido
    except Exception as e:
        print(f"Error al leer el archivo {ruta}: {e}")
        return []
    
# Necesito crear en siguiente formato en la hoja FX para las columnas
# ID, Nombre proveedor, TAX ID, Invoice, Fecha, Moneda, Total
# Dentro de la columna proveedor necesito que se almacene el nombre del proveedor encontrado
# En Tax ID, los datos de Tax ID o Cedula Juridica que se hayan encontrado de acuerdo al proveedor y rango asinado en atributos.txt
# Siguiendo la logica de Tax ID, En la columna invoice los datos: invoice o numero interno o invoice no o invoice number
# En la columna Fecha, los datos: Date o Fecha o Invoice Date
# En la columna Moneda, los datos: Moneda, Currency, y si al encontrar la palabra USD es True, ponerla
# En la columna total, los datos: Due,Total, Total Amount, Amount due

#Vamos poco a poco, primero necesito que me digas en que archivo deberia correguir, despues como crear la estructura del excel en la hoja fx y al final como asignar los atributos.txt a cada columna