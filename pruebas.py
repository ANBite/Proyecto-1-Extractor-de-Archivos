import os
import time
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import customtkinter as ctk

def obtener_info_gif(ruta_gif):
    try:
        with open(ruta_gif, 'rb') as f:
            version = f.read(6).decode('utf-8')
            width = int.from_bytes(f.read(2), 'little')
            height = int.from_bytes(f.read(2), 'little')
            packed_field = f.read(1)[0]
            bits_per_pixel = (packed_field & 0b00000111) + 1
            has_global_color_table = (packed_field & 0b10000000) != 0
            if has_global_color_table:
                color_table_size = 2 ** ((packed_field & 0b00000111) + 1)
                f.read(3 * color_table_size)
            background_color_index = f.read(1)[0]
            comentarios = "No hay comentarios"
            while True:
                byte = f.read(1)
                if byte == b'\x21':
                    extension_label = f.read(1)
                    if extension_label == b'\xfe':
                        comentarios = ""
                        block_size = f.read(1)[0]
                        while block_size != 0:
                            comentario = f.read(block_size).decode('utf-8', 'ignore')
                            comentarios += comentario
                            block_size = f.read(1)[0]
                elif byte == b'\x2c':
                    break
                elif byte == b'\x3b':
                    break
            fecha_creacion = time.ctime(os.path.getctime(ruta_gif))
            fecha_modificacion = time.ctime(os.path.getmtime(ruta_gif))
            
            return {
                "Número de versión": version,
                "Tamaño de imagen": (width, height),
                "Bits por pixel": bits_per_pixel,
                "Color de fondo (índice)": background_color_index,
                "Comentarios": comentarios,
                "Fecha de creación": fecha_creacion,
                "Fecha de modificación": fecha_modificacion
            }
    except Exception as e:
        return {"error": str(e)}

def abrir_gifs():
    rutas_gifs = filedialog.askopenfilenames(filetypes=[("GIF files", "*.gif")])
    if rutas_gifs:
        for ruta in rutas_gifs:
            info = obtener_info_gif(ruta)
            mostrar_info_y_gif(ruta, info)

def mostrar_info_y_gif(ruta, info):
    # Crear un marco dentro del marco desplazable para cada GIF e información
    gif_frame = ctk.CTkFrame(scrollable_frame)
    gif_frame.pack(pady=10, padx=10, fill="both")

    # Mostrar la información del GIF en etiquetas
    info_text = f"{'Archivo:':<15} {ruta}\n"
    for clave, valor in info.items():
        info_text += f"{clave:<25} {str(valor):<25}\n"
    
    info_label = ctk.CTkLabel(gif_frame, text=info_text, anchor="w", justify="left")
    info_label.pack(pady=5)

    # Mostrar el GIF
    gif = Image.open(ruta)
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))
    except EOFError:
        pass

    gif_label = Label(gif_frame)
    gif_label.pack()

    def actualizar_frame(indice):
        frame = frames[indice]
        gif_label.config(image=frame)
        gif_label.image = frame
        ventana.after(100, actualizar_frame, (indice + 1) % len(frames))

    if frames:
        actualizar_frame(0)

# Configuración de la interfaz gráfica
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Lector de GIFs (Bytes)")
ventana.geometry("800x600")

boton_abrir = ctk.CTkButton(ventana, text="Abrir GIFs", command=abrir_gifs)
boton_abrir.pack(pady=20)

# Crear un marco desplazable para mostrar la información y los GIFs
scrollable_frame = ctk.CTkScrollableFrame(ventana, width=750, height=500)
scrollable_frame.pack(pady=20, padx=10)

ventana.mainloop()

