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
            mostrar_info(ruta, info)
            mostrar_gif(ruta)

def abrir_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        for root, _, files in os.walk(carpeta):
            for file in files:
                if file.lower().endswith(".gif"):
                    ruta_gif = os.path.join(root, file)
                    info = obtener_info_gif(ruta_gif)
                    mostrar_info(ruta_gif, info)
                    mostrar_gif(ruta_gif)

def mostrar_info(ruta, info):
    info_text = f"{'Archivo:':<15} {ruta}\n"
    for clave, valor in info.items():
        info_text += f"{clave:<25} {str(valor):<25}\n"
    info_text += "\n" + "-"*50 + "\n"
    
    info_label = ctk.CTkLabel(info_frame, text=info_text, anchor="w", justify="left")
    info_label.pack(pady=5, padx=5)

def mostrar_gif(ruta_gif):
    gif = Image.open(ruta_gif)
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))
    except EOFError:
        pass

    gif_label = Label(gif_frame)
    gif_label.pack(pady=5, padx=5)

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
ventana.geometry("1000x600")

# Botones para abrir archivos GIF individuales o una carpeta
boton_abrir = ctk.CTkButton(ventana, text="Abrir GIFs", command=abrir_gifs)
boton_abrir.pack(pady=5)
boton_abrir_carpeta = ctk.CTkButton(ventana, text="Abrir Carpeta de GIFs", command=abrir_carpeta)
boton_abrir_carpeta.pack(pady=5)

# Marcos desplazables para mostrar la información y los GIFs
info_frame = ctk.CTkScrollableFrame(ventana, width=450, height=500)
info_frame.pack(side="left", padx=10, pady=10)
gif_frame = ctk.CTkScrollableFrame(ventana, width=450, height=500)
gif_frame.pack(side="right", padx=10, pady=10)

ventana.mainloop()
