import os
import time
from tkinter import filedialog
import customtkinter as ctk

def obtener_info_gif(ruta_gif):
    try:
        with open(ruta_gif, 'rb') as f:
            # Leer los primeros 6 bytes para obtener la versión del GIF (GIF87a o GIF89a)
            version = f.read(6).decode('utf-8')
            
            # Leer el tamaño de la imagen (anchura y altura) - 2 bytes cada uno (Little Endian)
            width = int.from_bytes(f.read(2), 'little')
            height = int.from_bytes(f.read(2), 'little')
            
            # Leer el byte del campo de descripción del paquete de imágenes
            packed_field = f.read(1)[0]
            
            # Obtener la cantidad de bits por pixel (de la paleta)
            bits_per_pixel = (packed_field & 0b00000111) + 1  # Bits per pixel
            cantidad_colores = 2 ** bits_per_pixel  # Cantidad de colores
            
            # Comprobar si tiene paleta global de colores
            has_global_color_table = (packed_field & 0b10000000) != 0
            
            # Leer la paleta global de colores si existe
            if has_global_color_table:
                color_table_size = 2 ** ((packed_field & 0b00000111) + 1)
                f.read(3 * color_table_size)  # Saltar la paleta global
            
            # Leer el color de fondo
            background_color_index = f.read(1)[0]
            
            # Contar la cantidad de imágenes y determinar el tipo de compresión
            cantidad_imagenes = 0
            tipo_compresion = "LZW"  # Los GIFs usan generalmente LZW

            comentarios = "No hay comentarios"
            while True:
                byte = f.read(1)
                if byte == b'\x21':  # Introducción de extensión (posiblemente comentario)
                    extension_label = f.read(1)
                    if extension_label == b'\xfe':  # Comentarios
                        comentarios = ""
                        block_size = f.read(1)[0]
                        while block_size != 0:
                            comentario = f.read(block_size).decode('utf-8', 'ignore')
                            comentarios += comentario
                            block_size = f.read(1)[0]
                elif byte == b'\x2c':  # Introducción de la imagen
                    cantidad_imagenes += 1
                elif byte == b'\x3b':  # Fin del archivo GIF
                    break
            
            # Fechas de creación y modificación del archivo
            fecha_creacion = time.ctime(os.path.getctime(ruta_gif))
            fecha_modificacion = time.ctime(os.path.getmtime(ruta_gif))
            
            # Formato numérico (hexadecimal y decimal)
            formato_numerico = f"Hex: {width:#04x}x{height:#04x}, Dec: {width}x{height}"
            
            return {
                "Número de versión": version,
                "Tamaño de imagen": (width, height),
                "Bits por pixel": bits_per_pixel,
                "Cantidad de colores": cantidad_colores,
                "Color de fondo (índice)": background_color_index,
                "Comentarios": comentarios,
                "Fecha de creación": fecha_creacion,
                "Fecha de modificación": fecha_modificacion,
                "Cantidad de imágenes": cantidad_imagenes,
                "Tipo de compresión": tipo_compresion,
                "Formato numérico": formato_numerico
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

# Función para mostrar la información en la interfaz en columnas
def mostrar_info(ruta, info):
    # Primero, muestra el nombre del archivo en la primera columna
    info_textbox.insert(ctk.END, f"{'Archivo:':<15} {ruta}\n")
    
    # Luego, muestra cada dato en una fila en columnas
    for clave, valor in info.items():
        # Formatea cada línea con espacios para alineación en columnas
        info_textbox.insert(ctk.END, f"{clave:<25} {str(valor):<25}\n")
        
    # Añade una línea divisoria entre archivos
    info_textbox.insert(ctk.END, "\n" + "-"*50 + "\n")

# Configuración de la interfaz gráfica
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Lector de GIFs (Bytes)")
ventana.geometry("600x500")

# Botón para abrir archivos GIF
boton_abrir = ctk.CTkButton(ventana, text="Abrir GIFs", command=abrir_gifs)
boton_abrir.pack(pady=20)

# Cuadro de texto para mostrar la información
info_textbox = ctk.CTkTextbox(ventana, width=500, height=300)
info_textbox.pack(pady=20)

ventana.mainloop()