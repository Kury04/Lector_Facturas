import pandas as pd
from columns_extractor import extraer_columnas
from xml_procesador.procesador import procesar_documentos


df_f43 = extraer_columnas()

# Procesar los documentos en la carpeta especificada
carpeta = "./resources/files"
progress_bar = None  # Si no usas una barra de progreso, puedes pasar None
_, df_palabras = procesar_documentos(carpeta, progress_bar)

# Realizar la unión
df_unido = pd.merge(
    df_f43,
    df_palabras,
    how='inner',
    left_on='Denominacion cuenta contrapartida',
    right_on='nombre_emisor'
)

# Verificar el resultado
print(df_unido.head())


