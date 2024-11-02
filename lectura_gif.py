import os
import time
import customtkinter as ctk


"""| Método para leer información en los gif |"""

def info_gif(ruta_gif, lugar_mostrar):
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

            label_text = {
                "Número de versión": version,
                "\nTamaño de imagen": size,
                "\nBits por pixel": color_resolution,
                "\nColores": num_colores,
                "\nCompresión": compresion,
                "\nColor de fondo (índice)": background_color_index,
                "\nNúmero de imágenes": num_imagenes,
                "\nFecha de creación": fecha_creacion,
                "\nFecha de modificación": fecha_modificacion,
                "\nComentarios": comentarios,
                "\nFormato numérico (Bits por pixel)": color_resolution
            }

            lugar_mostrar.configure(state=ctk.NORMAL)
            lugar_mostrar.delete(1.0, ctk.END)
            lugar_mostrar.insert(ctk.END, label_text)
            lugar_mostrar.configure(state=ctk.DISABLED)

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