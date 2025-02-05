import tkinter as tk
from tkinter import filedialog, messagebox
import os
from main import 

def seleccionar_carpeta():
    carpeta_seleccionada = filedialog.askdirectory()
    if carpeta_seleccionada:
        entrada_carpeta.delete(0, tk.END)
        entrada_carpeta.insert(0, carpeta_seleccionada)

def procesar_carpeta():
    carpeta = entrada_carpeta.get()
    if not carpeta or not os.path.exists(carpeta):
        messagebox.showerror("Error", "Por favor, seleccione una carpeta válida.")
        return
    messagebox.showinfo("Éxito", f"Carpeta seleccionada: {carpeta}")

# Crear ventana
ventana = tk.Tk()
ventana.title("Seleccionar Carpeta")
ventana.geometry("400x200")

# Etiqueta
etiqueta = tk.Label(ventana, text="Ingrese o seleccione la ruta:")
etiqueta.pack(pady=5)

# Campo de entrada
entrada_carpeta = tk.Entry(ventana, width=50)
entrada_carpeta.pack(pady=5)

# Botón para seleccionar carpeta
boton_seleccionar = tk.Button(ventana, text="Examinar", command=seleccionar_carpeta)
boton_seleccionar.pack(pady=5)

# Botón para procesar carpeta
boton_procesar = tk.Button(ventana, text="Procesar", command=procesar_carpeta)
boton_procesar.pack(pady=5)

# Ejecutar la ventana
ventana.mainloop()
