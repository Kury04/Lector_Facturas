import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PDF_procesador.file_utils import buscar_pdfs_en_carpeta
from PDF_procesador.pdf_utils import extraer_texto_pdf
from PDF_procesador.keyword_extractor import extraer_valores
from xml_procesador.procesador import procesar_cfdis
from xml_procesador.exportar_excel import crear_excel
from utils.archivos import leer_archivo

def seleccionar_carpeta():
    carpeta_seleccionada = filedialog.askdirectory()
    if carpeta_seleccionada:
        entrada_carpeta.delete(0, ctk.END)
        entrada_carpeta.insert(0, carpeta_seleccionada)

def procesar_carpeta():
    carpeta = entrada_carpeta.get()
    if not carpeta or not os.path.exists(carpeta):
        messagebox.showerror("Error", "Por favor, seleccione una carpeta válida.")
        return
    
    ruta_atributos = "resources/atributos.txt"
    archivo_proveedores = "resources/proveedores_extranjeros.txt"
    ruta_excel = "resources/files/prueba_excel.xlsx"
    
    palabras_clave = leer_archivo(ruta_atributos)
    proveedores = leer_archivo(archivo_proveedores)
    datos_facturas = procesar_cfdis(carpeta)
    datos_palabras = []
    
    if palabras_clave:
        archivos_pdf = buscar_pdfs_en_carpeta(carpeta)
        archivos_txt_generados = []
        
        for ruta_pdf in archivos_pdf:
            nombre_txt = os.path.basename(ruta_pdf).replace('.pdf', '.txt')
            ruta_txt = os.path.join(carpeta, nombre_txt)
            archivos_txt_generados.append(ruta_txt)
            
            texto_pdf = extraer_texto_pdf(ruta_pdf, ruta_txt)
            if texto_pdf:
                with open(ruta_txt, 'r') as archivo_txt:
                    texto_txt = archivo_txt.read()
                
                for proveedor_encontrado_str in proveedores:
                    if proveedor_encontrado_str in texto_txt:
                        rangos_proveedores = {
                            "C.H. Robinson": (1, 5),
                            "SOLUTRANS LOGISTICS S,A": (7, 11),
                            "SAMSUNG SDS AMERICA, INC.": (13, 16),
                            "Laredo, TX": (18, 24)
                        }
                        
                        if proveedor_encontrado_str in rangos_proveedores:
                            rango_busqueda = rangos_proveedores[proveedor_encontrado_str]
                            resultados = extraer_valores(ruta_txt, ruta_atributos, proveedor_encontrado_str, rango=rango_busqueda)
                            
                            if resultados:
                                resultados["Archivo"] = os.path.basename(ruta_txt)
                                datos_palabras.append(resultados)
                        break
        
        for ruta_txt in archivos_txt_generados:
            try:
                os.remove(ruta_txt)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar {ruta_txt}: {e}")
    
    if datos_facturas or datos_palabras:
        crear_excel(datos_facturas, datos_palabras, ruta_excel)
        messagebox.showinfo("Éxito", f"Datos exportados a {ruta_excel}")
    else:
        messagebox.showwarning("Atención", "No se encontraron datos para exportar.")

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear ventana
ventana = ctk.CTk()
ventana.title("Procesador de Facturas")
ventana.geometry("500x250")

# Etiqueta
etiqueta = ctk.CTkLabel(ventana, text="Ingrese o seleccione la ruta de la carpeta:")
etiqueta.pack(pady=5)

# Campo de entrada
entrada_carpeta = ctk.CTkEntry(ventana, width=400)
entrada_carpeta.pack(pady=5)

# Botón para seleccionar carpeta
boton_seleccionar = ctk.CTkButton(ventana, text="Examinar", command=seleccionar_carpeta)
boton_seleccionar.pack(pady=5)

# Botón para procesar carpeta
boton_procesar = ctk.CTkButton(ventana, text="Procesar", command=procesar_carpeta)
boton_procesar.pack(pady=5)

# Ejecutar la ventana
ventana.mainloop()
