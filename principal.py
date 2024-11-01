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
fondo = util_imagen.leer_imagen("./imagenes/imgfondo.jpg", (1950,1150))
background_label = ctk.CTkLabel(master=window, text="",image=fondo, width=0, height=0)
background_label.place(relx=0, rely=0, relwidth=1, relheight=1)


"""| Cajas de texto |"""
def scrool(event):
    # Desplazarse verticalmente con la rueda del mouse
    box1.yview_scroll(int(-1*(event.delta/120)), "units")


def zoom(event):
    global size #Tamaño de las letras
    if event.delta > 0 :
        size += 1
    else:
        size -= 1
    box1.configure(font=("Times New Roman", size))
    
size = 12 #Tamaño original de las letras

box1 = ctk.CTkTextbox(master=window, wrap=ctk.NONE, font=("Times New Roman", size), width=300, height=760)
box1.place(x=10, y=10)

box1.bind("<MouseWheel>", scrool)


window.bind("<Control-MouseWheel>", zoom)
window.mainloop() #Se inicializa la ventana