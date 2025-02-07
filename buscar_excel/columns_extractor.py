import pandas as pd

def extraer_columnas(df_f43=None, df_operaciones= None):
    # Rutas
    excel_f43 = "resources/files/F-43.xlsx"
    opera_expor = "resources/files/OPERACIONES DE EXPORTACION 2025.xlsx"

    # Columnas
    columnas_f43 = ['Cta CP (SAP)', 'Denominacion cuenta contrapartida', 'Centro coste', 'Cl coste']
    columnas_operaciones = ['Unnamed: 25', 'Unnamed: 40']

    # Leer datos
    try:
        df_f43 = pd.read_excel(excel_f43, sheet_name='Acreedores SAP', usecols=columnas_f43)
        df_operaciones = pd.read_excel(opera_expor, sheet_name='ENERO', usecols=columnas_operaciones)

        # Imprimir resultados
        print(df_f43)
        print(df_operaciones)

        return df_f43, df_operaciones
    except Exception as e:
        print(f"Error al leer los datos: {e}")



