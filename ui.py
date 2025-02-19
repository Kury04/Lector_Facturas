import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import json
from buscar_excel.unir_df import buscar_columnas

# Ruta del archivo de configuración
CONFIG_FILE = "config.json"

def cargar_configuracion():
    """Carga la configuración desde el archivo JSON."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_configuracion(config):
    """Guarda la configuración en un archivo JSON."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def seleccionar_archivo(entrada):
    """Abre un diálogo para seleccionar un archivo y actualiza la entrada."""
    archivo_seleccionado = filedialog.askopenfilename()
    if archivo_seleccionado:
        entrada.delete(0, ctk.END)
        entrada.insert(0, archivo_seleccionado)

def abrir_configuracion():
    """Abre una subventana para configurar las rutas de los archivos."""
    config = cargar_configuracion()

    # Crear subventana
    subventana = ctk.CTkToplevel()
    subventana.title("Configuración de Rutas")
    subventana.geometry("500x400")

    # Crear un frame desplazable
    scrollable_frame = ctk.CTkScrollableFrame(subventana, width=450, height=350)
    scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Variables para almacenar las rutas ingresadas
    rutas = {
        "EXCEL_F43": ctk.StringVar(value=config.get("EXCEL_F43", "")),
        "EXCEL_EXPORT": ctk.StringVar(value=config.get("EXCEL_EXPORT", "")),
        "EXCEL_IMPORT": ctk.StringVar(value=config.get("EXCEL_IMPORT", "")),
        "EXCEL_TC": ctk.StringVar(value=config.get("EXCEL_TC", "")),
        "ATRIBUTOS": ctk.StringVar(value=config.get("ATRIBUTOS", "")),
        "PROVEEDORES_EXTRANJEROS": ctk.StringVar(value=config.get("PROVEEDORES_EXTRANJEROS", "")),
    }

    # Función para guardar la configuración
    def guardar_config():
        nueva_config = {
            "EXCEL_F43": rutas["EXCEL_F43"].get(),
            "EXCEL_EXPORT": rutas["EXCEL_EXPORT"].get(),
            "EXCEL_IMPORT": rutas["EXCEL_IMPORT"].get(),
            "EXCEL_TC": rutas["EXCEL_TC"].get(),
            "ATRIBUTOS": rutas["ATRIBUTOS"].get(),
            "PROVEEDORES_EXTRANJEROS": rutas["PROVEEDORES_EXTRANJEROS"].get(),
        }
        guardar_configuracion(nueva_config)
        messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
        subventana.destroy()

    # Campos para seleccionar archivos (dentro del frame desplazable)
    ctk.CTkLabel(scrollable_frame, text="Ruta de F-43.xlsx:").pack(pady=5)
    entrada_f43 = ctk.CTkEntry(scrollable_frame, width=400, textvariable=rutas["EXCEL_F43"])
    entrada_f43.pack(pady=5)
    ctk.CTkButton(scrollable_frame, text="Seleccionar", command=lambda: seleccionar_archivo(entrada_f43)).pack(pady=5)

    ctk.CTkLabel(scrollable_frame, text="Ruta de OPERACIONES DE EXPORTACION 2025.xlsx:").pack(pady=5)
    entrada_export = ctk.CTkEntry(scrollable_frame, width=400, textvariable=rutas["EXCEL_EXPORT"])
    entrada_export.pack(pady=5)
    ctk.CTkButton(scrollable_frame, text="Seleccionar", command=lambda: seleccionar_archivo(entrada_export)).pack(pady=5)

    ctk.CTkLabel(scrollable_frame, text="Ruta de OPERACIONES DE IMPORTACION 2025.xlsx:").pack(pady=5)
    entrada_import = ctk.CTkEntry(scrollable_frame, width=400, textvariable=rutas["EXCEL_IMPORT"])
    entrada_import.pack(pady=5)
    ctk.CTkButton(scrollable_frame, text="Seleccionar", command=lambda: seleccionar_archivo(entrada_import)).pack(pady=5)

    ctk.CTkLabel(scrollable_frame, text="Ruta de TC.xlsx:").pack(pady=5)
    entrada_tc = ctk.CTkEntry(scrollable_frame, width=400, textvariable=rutas["EXCEL_TC"])
    entrada_tc.pack(pady=5)
    ctk.CTkButton(scrollable_frame, text="Seleccionar", command=lambda: seleccionar_archivo(entrada_tc)).pack(pady=5)

    ctk.CTkLabel(scrollable_frame, text="Ruta de atributos.txt:").pack(pady=5)
    entrada_atributos = ctk.CTkEntry(scrollable_frame, width=400, textvariable=rutas["ATRIBUTOS"])
    entrada_atributos.pack(pady=5)
    ctk.CTkButton(scrollable_frame, text="Seleccionar", command=lambda: seleccionar_archivo(entrada_atributos)).pack(pady=5)

    ctk.CTkLabel(scrollable_frame, text="Ruta de proveedores_extranjeros.txt:").pack(pady=5)
    entrada_proveedores = ctk.CTkEntry(scrollable_frame, width=400, textvariable=rutas["PROVEEDORES_EXTRANJEROS"])
    entrada_proveedores.pack(pady=5)
    ctk.CTkButton(scrollable_frame, text="Seleccionar", command=lambda: seleccionar_archivo(entrada_proveedores)).pack(pady=5)

        # Botón para guardar la configuración (dentro del scrollable_frame)
    boton_guardar = ctk.CTkButton(scrollable_frame, text="Guardar", command=guardar_config)
    boton_guardar.pack(pady=10)  # Añade un margen vertical
    
def seleccionar_carpeta(entrada):
    """Abre un diálogo para seleccionar una carpeta y actualiza la entrada."""
    carpeta_seleccionada = filedialog.askdirectory()
    if carpeta_seleccionada:
        entrada.delete(0, ctk.END)
        entrada.insert(0, carpeta_seleccionada)

def iniciar_proceso(entrada, progress_bar, ventana):
    """Inicia el procesamiento de archivos."""
    carpeta = entrada.get()
    if not carpeta or not os.path.exists(carpeta):
        messagebox.showerror("Error", "Por favor, seleccione una carpeta válida.")
        return
    
    # Iniciar barra de progreso en modo indeterminado
    progress_bar.set(0)
    progress_bar.start()
    ventana.update_idletasks()  # Actualizar UI antes de procesar

    try:
        buscar_columnas(carpeta, progress_bar)  # Pasamos progress_bar a la función
        progress_bar.stop()  # Detener animación cuando termina
        progress_bar.set(1)  # Marcar progreso completado

        messagebox.showinfo("Éxito", f"Procesamiento completado en {carpeta}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        progress_bar.stop()  # Detener barra en caso de error
        progress_bar.set(0)

def iniciar_interfaz():
    """Inicia la interfaz principal."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Procesador de Facturas")
    ventana.geometry("500x350")

    # Botón para abrir la configuración
    boton_configuracion = ctk.CTkButton(ventana, text="Configuración", command=abrir_configuracion)
    boton_configuracion.pack(pady=10)

    etiqueta = ctk.CTkLabel(ventana, text="Ingrese o seleccione la ruta de la carpeta:")
    etiqueta.pack(pady=5)

    entrada_carpeta = ctk.CTkEntry(ventana, width=400)
    entrada_carpeta.pack(pady=5)

    boton_seleccionar = ctk.CTkButton(ventana, text="Examinar", command=lambda: seleccionar_carpeta(entrada_carpeta))
    boton_seleccionar.pack(pady=5)

    progress_bar = ctk.CTkProgressBar(ventana, width=400)
    progress_bar.set(0)
    progress_bar.pack(pady=10)

    boton_procesar = ctk.CTkButton(
        ventana, text="Procesar",
        command=lambda: iniciar_proceso(entrada_carpeta, progress_bar, ventana)
    )
    boton_procesar.pack(pady=5)

    ventana.mainloop()