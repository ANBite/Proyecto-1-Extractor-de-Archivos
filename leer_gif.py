import os
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, GifImagePlugin
import time

# Función para extraer la información del GIF
def obtener_info_gif(ruta_gif):
    try:
        with Image.open(ruta_gif) as img:
            if isinstance(img, GifImagePlugin.GifImageFile):
                # Tamaño de imagen
                size = img.size
                
                # Número de colores (paleta de colores)
                if img.getpalette():
                    num_colores = len(img.getpalette()) // 3  # La paleta tiene 3 valores por color (RGB)
                else:
                    num_colores = 'No disponible'

                # Cantidad de imágenes en el GIF (frames)
                num_imagenes = img.n_frames
                
                # Tipo de compresión (GIF usa LZW por defecto)
                compresion = img.info.get("compression", "LZW")
                
                # Color de fondo
                color_fondo = img.info.get("background", "No especificado")
                
                # Comentarios (si los hay)
                comentarios = img.info.get("comment", "No hay comentarios")
                
                # Fechas de creación y modificación
                fecha_creacion = time.ctime(os.path.getctime(ruta_gif))
                fecha_modificacion = time.ctime(os.path.getmtime(ruta_gif))
                
                return {
                    "Tamaño": size,
                    "Colores": num_colores,
                    "Compresión": compresion,
                    "Color de fondo": color_fondo,
                    "Número de imágenes": num_imagenes,
                    "Fecha de creación": fecha_creacion,
                    "Fecha de modificación": fecha_modificacion,
                    "Comentarios": comentarios
                }
    except Exception as e:
        return {"error": str(e)}

# Función para abrir archivo y mostrar la información
def abrir_gifs():
    rutas_gifs = filedialog.askopenfilenames(filetypes=[("GIF files", "*.gif")])
    if rutas_gifs:
        for ruta in rutas_gifs:
            info = obtener_info_gif(ruta)
            mostrar_info(ruta, info)

# Función para mostrar la información en la interfaz
def mostrar_info(ruta, info):
    info_textbox.insert(ctk.END, f"\nArchivo: {ruta}\n")
    for clave, valor in info.items():
        info_textbox.insert(ctk.END, f"{clave}: {valor}\n")
    info_textbox.insert(ctk.END, "\n" + "-"*50 + "\n")

# Configuración de la interfaz gráfica
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Lector de GIFs")
ventana.geometry("600x500")

# Botón para abrir archivos GIF
boton_abrir = ctk.CTkButton(ventana, text="Abrir GIFs", command=abrir_gifs)
boton_abrir.pack(pady=20)

# Cuadro de texto para mostrar la información
info_textbox = ctk.CTkTextbox(ventana, width=500, height=300)
info_textbox.pack(pady=20)

ventana.mainloop()
