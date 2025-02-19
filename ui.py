import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from buscar_excel.unir_df import buscar_columnas

def seleccionar_carpeta(entrada):
    carpeta_seleccionada = filedialog.askdirectory()
    if carpeta_seleccionada:
        entrada.delete(0, ctk.END)
        entrada.insert(0, carpeta_seleccionada)

def iniciar_proceso(entrada, progress_bar, ventana):
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
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Procesador de Facturas")
    ventana.geometry("500x300")

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

