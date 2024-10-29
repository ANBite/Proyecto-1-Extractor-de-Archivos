"""| Se importan las librerías para la interfáz gráfica: |"""
import customtkinter as ctk #CustomTkinter para la parte gráfica

import utilidades.utilidad_ventana as util_ventana #Archivo para que quede centrada la ventana
import utilidades.utilidad_imagen as util_imagen #Archivo para que las imágenes sean compatibles


"""| Ventana principal |"""
window = ctk.CTkToplevel() #Se crea la ventana
window.geometry("1550x850") #Se da el tamaño a la ventana
window.title("Extractor de Archivos GIF") #Se le asigna un nombre a la ventana
window.resizable(True, True)
window.grab_set() #Queda debajo de cualquier ventana que se abra
util_ventana.centrar_ventana(window, 1550, 850)
fondo = util_imagen.leer_imagen("./imagenes/imgfondo.jpg", (50,40))
background_label = ctk.CTkLabel(master=window, image=fondo, text="", width=0, height=0)




window.mainloop() #Se inicializa la ventana