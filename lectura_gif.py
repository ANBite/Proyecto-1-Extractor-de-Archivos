"""| Se importan las librerías necesarias |"""
import os #Necesario para abrir un archivo
import time #Para saber en que momento fue modificado el archivo
import customtkinter as ctk #Para mostrar la información obtenida

l_archivo = [] #Lista para tener el nombre de los archivos
l_version = [] #Lista para tener todas las versiones
l_tamanio = [] #Lista para tener todos los tamaños
l_cantcolores = [] #Lista para tener la cantidad de colores
l_comprension = [] #Lista para la comprensión del archivo
l_formatonumeric = [] #Lista para el formato numérico
l_colorfondo = [] #Lista para color de fondo
l_nimagenes = [] #Lista para numero de imagenes que contiene
l_creacion = [] #Lita para la fecha de creacion
l_modificacion = [] #Lista para la fecha de modificación
l_comentarios = [] #Lista para los comentarios


"""| Método para leer información en los gif |"""


def info_gif(ruta_gif):
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
                          localcolor_table_size = 2 ** ((img_field & 0b00000111) + 1)
                          file.read(3 * localcolor_table_size)
                    while True:
                        sub_block_size = file.read(1)[0]
                        if sub_block_size == 0:
                             break
                        file.read(sub_block_size)
                elif byte == b"\x3b": #Fin del archivo
                     break
            f_creation = time.ctime(os.path.getctime(ruta_gif)) #Se obtiene la fecha de creación
            f_modification = time.ctime(os.path.getmtime(ruta_gif)) #Se obtiene la fecha de modificación

            comprension = "LZW"
            archivo = ruta_gif


            l_archivo.append(archivo)
            l_version.append(version)
            l_tamanio.append(size_gif)
            l_cantcolores.append(num_colors)
            l_comprension.append(comprension)
            l_formatonumeric.append(color_resolution)
            l_colorfondo.append(background_color)
            l_nimagenes.append(num_imgs)
            l_creacion.append(f_creation)
            l_modificacion.append(f_modification)
            l_comentarios.append(comments)
    


def showinfo(ruta_gif, lugar_print):

    info_gif(ruta_gif)

    c = len(l_archivo)
    print(c)

    lugar_print.configure(state=ctk.NORMAL)
    lugar_print.delete(1.0, ctk.END)

    for i in range(c):
        lugar_print.insert(ctk.END, f"\n---------- GIF #{i+1} ----------")
        lugar_print.insert(ctk.END, f"\nArchivo: {l_archivo[i]}")
        lugar_print.insert(ctk.END, f"\nVersión: {l_version[i]}")
        lugar_print.insert(ctk.END, f"\nTamaño de imagen: {l_tamanio[i]}")
        lugar_print.insert(ctk.END, f"\nCantidad de colores: {l_cantcolores[i]}")
        lugar_print.insert(ctk.END, f"\nComprensión: {l_comprension[i]}")
        lugar_print.insert(ctk.END, f"\nFormato de imagen: {l_formatonumeric[i]}")
        lugar_print.insert(ctk.END, f"\nColor de fondo: {l_colorfondo[i]}")
        lugar_print.insert(ctk.END, f"\nNúmero de imágenes: {l_nimagenes[i]}")
        lugar_print.insert(ctk.END, f"\nFecha de creación: {l_creacion[i]}")
        lugar_print.insert(ctk.END, f"\nFecha de modificación: {l_modificacion[i]}")        
        lugar_print.insert(ctk.END, f"\nComentarios: {l_comentarios[i]}\n") 



    lugar_print.configure(state=ctk.DISABLED)
     