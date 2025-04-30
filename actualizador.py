import requests
import os
import json

# 🔹 Configuración
OWNER = "Kury04"  # Tu usuario de GitHub
REPO = "EJECUTABLE"  # Tu repositorio de GitHub
ARCHIVO = "main.py"  # Nombre del ejecutable
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
VERSION_ACTUAL = "v1.0.0"


def obtener_ultima_version():
    """Obtiene la última versión desde GitHub Releases"""
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data["tag_name"], data["assets"][0]["browser_download_url"]
    return None, None

def actualizar_programa():
    """Descarga y reemplaza main.py si hay una versión más reciente"""
    ultima_version, url_descarga = obtener_ultima_version()
    if ultima_version and url_descarga and ultima_version != VERSION_ACTUAL:
        print(f"📥 Nueva versión disponible: {ultima_version}. Descargando...")
        response = requests.get(url_descarga)
        with open(ARCHIVO, "wb") as file:
            file.write(response.content)
        print("✅ Actualización completada. Reiniciando...")
        os.system(f"python {ARCHIVO}")  # Ejecutar el nuevo código
        exit()
    else:
        print("✅ El programa ya está actualizado.")

# 🔄 Verifica actualizaciones antes de ejecutar el código principal
actualizar_programa()

# 🔹 Código normal de main.py (se ejecuta solo si no hubo actualización)
print("Ejecutando la aplicación...")
# Resto de tu código aquí
