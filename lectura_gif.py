"""| Se importan las librerías necesarias |"""
import os #Necesario para abrir un archivo
import time #Para saber en que momento fue modificado el archivo
import customtkinter as ctk #Para mostrar la información obtenida

"""| Método para leer información en los gif |"""
def info_gif(ruta_gif, lugar_print):
    with open(ruta_gif, "rb") as file: #Se abre el archivo
            version = file.read(6).decode("utf-8") #Se leen los 6 primeros bytes
            
            width = int.from_bytes(file.read(2), "little") #Se lee el ancho del gif
            height = int.from_bytes(file.read(2), "little") #Se lee el alto del gif
            size_gif = (width, height) #Tamaño de la imagen

            field = file.read(1)[0] #Campo para leer los siguientes bytes
            color_table = (field & 0b10000000) != 0 #Paleta de colores
            color_resolution = ((field & 0b01110000 >> 4)) + 1 #Resolución de color
            color_table_size = 2 ** ((field & 0b00000111) + 1) #Tamaño de la paleta de colores
            background_color = file.read(1)[0] #Color de fondo

            if color_table:
                  file.read(3 * color_table_size)
            num_colors = color_table_size if color_table else "No tiene paleta de colores" #Cuantos colores tiene

            num_imgs = 0 #Cantidad de imagenes en el gif (por defecto 0)
            comments = "No hay comentarios" #Comentarios en el gif (por defecto no hay)

            while True:
                byte = file.read(1)
                if byte == b"\x21" : #Bloque de extensión
                    extension = file.read(1) #Extención del archivo gif
                    if extension == b"\xfe": #Verifica si hay comentarios
                        comments = "" 
                        block_size = file.read(1)[0]
                        while block_size != 0:
                             comment = file.read(block_size).decode("utf-8", "ignore")
                             comments += comment #Agrega el comentario que está en el gif
                             block_size = file.read(1)[0]
                    elif extension == b"\xf9": #Bloque de control gráfico
                         file.read(6)
                elif byte == b"\x2c":
                     num_imgs += 1
                     file.read(9)
                     img_field = file.read(1)[0]
                     if img_field & 0b10000000:
                          color_table_size = 2