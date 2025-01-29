# Buscar y procesar archivos PDF
archivos_pdf = buscar_pdfs_en_carpeta(carpeta)
archivos_txt_generados = []  # Lista para almacenar los archivos TXT generados

for ruta_pdf in archivos_pdf:
    nombre_txt = os.path.basename(ruta_pdf).replace('.pdf', '.txt')
    ruta_txt = os.path.join(carpeta, nombre_txt)
    archivos_txt_generados.append(ruta_txt)  # Guardar la ruta del archivo TXT

    # Extraer texto del PDF y guardarlo en un archivo TXT
    texto_pdf = extraer_texto_pdf(ruta_pdf, ruta_txt)
    if texto_pdf:
        print(f"Archivo PDF convertido a TXT: {ruta_txt}")  # Depuración

        # Leer el archivo TXT
        with open(ruta_txt, 'r') as archivo_txt:
            texto_txt = archivo_txt.read()

        # Validar si el archivo TXT contiene algún proveedor extranjero
        proveedor_encontrado = False
        for proveedor in proveedores:
            if proveedor in texto_txt:
                proveedor_encontrado = True
                print(f"Proveedor encontrado: {proveedor}")
                break

        # Buscar palabras clave en el archivo TXT
        resultados = extraer_valores(ruta_txt, palabras_clave)

        # Imprimir resultados - Depuración
        print(f"\nResultados para {os.path.basename(ruta_pdf)}:")
        for palabra, valor in resultados.items():
            print(f"  {palabra}: {valor}")

        # Verificar palabras clave específicas
        palabras_verificar = ["USD", "DOB001109DK5"]
        booleans = verificar_palabras_clave(ruta_txt, palabras_verificar)
        print("\nPresencia de palabras específicas:")
        for palabra, encontrado in booleans.items():
            print(f"  {palabra}: {True if encontrado else False}")  # Depuración

        print(f"El archivo TXT generado está en: {ruta_txt}")  # Depuración

# Eliminar todos los archivos TXT generados
for ruta_txt in archivos_txt_generados:
    try:
        os.remove(ruta_txt)
        print(f"Archivo TXT eliminado: {ruta_txt}")  # Depuración
    except Exception as e:
        print(f"Error al eliminar el archivo TXT {ruta_txt}: {e}")  # Depuración