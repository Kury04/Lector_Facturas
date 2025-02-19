import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construcción de rutas dinámicas
EXCEL_F43 = os.path.join(BASE_DIR, "resources", "files", "F-43.xlsx")
EXCEL_EXPORT = os.path.join(BASE_DIR, "resources", "files", "OPERACIONES DE EXPORTACION 2025.xlsx")
EXCEL_IMPORT = os.path.join(BASE_DIR, "resources", "files", "OPERACIONES DE IMPORTACION 2025.xlsx")
EXCEL_TC = os.path.join(BASE_DIR, "resources", "files", "TC.xlsx")
ATRIBUTOS = os.path.join(BASE_DIR, "resources", "atributos.txt")
PROVEEDORES_EXTRANJEROS = os.path.join(BASE_DIR, "resources", "proveedores_extranjeros.txt")
