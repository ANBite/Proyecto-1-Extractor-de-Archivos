import os
import time
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import customtkinter as ctk

def obtener_info_gif(ruta_gif):
    try:
        with open(ruta_gif, 'rb') as f:
            # Leer encabezado y versión
            version = f.read(6).decode('utf-8')
            if version[:3] != 'GIF':
                return {"error": "Archivo no es un GIF válido"}
            
            # Tamaño de la imagen (ancho y alto)
            width = int.from_bytes(f.read(2), 'little')
            height = int.from_bytes(f.read(2), 'little')
            size = (width, height)

            # Campo empaquetado, índice de color de fondo y relación de aspecto de píxel
            packed_field = f.read(1)[0]
            has_global_color_table = (packed_field & 0b10000000) != 0
            color_resolution = ((packed_field & 0b01110000) >> 4) + 1
            color_table_size = 2 ** ((packed_field & 0b00000111) + 1)
            background_color_index = f.read(1)[0]

            # Leer la paleta de colores global si está presente
            if has_global_color_table:
                f.read(3 * color_table_size)
            num_colores = color_table_size if has_global_color_table else 'No disponible'

            # Obtener comentarios y contar número de imágenes
            num_imagenes = 0
            comentarios = "No hay comentarios"
            while True:
                byte = f.read(1)
                if byte == b'\x21':  # Bloque de extensión
                    extension_label = f.read(1)
                    if extension_label == b'\xfe':  # Comentarios
                        comentarios = ""
                        block_size = f.read(1)[0]
                        while block_size != 0:
                            comentario = f.read(block_size).decode('utf-8', 'ignore')
                            comentarios += comentario
                            block_size = f.read(1)[0]
                    elif extension_label == b'\xf9':  # Bloque de control gráfico
                        f.read(6)  # Saltar datos del bloque de control gráfico
                elif byte == b'\x2c':  # Bloque de imagen (frame)
                    num_imagenes += 1
                    f.read(9)  # Saltar datos de imagen
                    packed_image_field = f.read(1)[0]
                    if packed_image_field & 0b10000000:  # Paleta local
                        local_color_table_size = 2 ** ((packed_image_field & 0b00000111) + 1)
                        f.read(3 * local_color_table_size)
                    while True:
                        sub_block_size = f.read(1)[0]
                        if sub_block_size == 0:
                            break
                        f.read(sub_block_size)
                elif byte == b'\x3b':  # Fin del archivo
                    break

            # Obtener fechas de creación y modificación
            fecha_creacion = time.ctime(os.path.getctime(ruta_gif))
            fecha_modificacion = time.ctime(os.path.getmtime(ruta_gif))

            # Compresión
            compresion = "LZW"

            return {
                "Número de versión": version,
                "Tamaño de imagen": size,
                "Bits por pixel": color_resolution,
                "Colores": num_colores,
                "Compresión": compresion,
                "Color de fondo (índice)": background_color_index,
                "Número de imágenes": num_imagenes,
                "Fecha de creación": fecha_creacion,
                "Fecha de modificación": fecha_modificacion,
                "Comentarios": comentarios,
                "Formato numérico (Bits por pixel)": color_resolution
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
