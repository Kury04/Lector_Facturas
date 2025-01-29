def leer_archivo(ruta):
    try:
        with open(ruta, 'r') as archivo:
            contenido = [line.strip() for line in archivo.readlines()]
        print(f"Se cargaron {len(contenido)} elementos desde {ruta}.")
        return contenido
    except Exception as e:
        print(f"Error al leer el archivo {ruta}: {e}")
        return []
