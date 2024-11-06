"""| Se importan las librerías para la interfáz gráfica: |"""
import customtkinter as ctk #CustomTkinter para la parte gráfica
from tkinter import filedialog
import os
from datos_archivo import Datos
import utilidades.utilidad_ventana as util_ventana #Archivo para que quede centrada la ventana
import utilidades.utilidad_imagen as util_imagen #Archivo para que las imágenes sean compatibles
from lectura_gif import showinfo
from mostrar_gif import show_gif
from write_txt import Write_txt

lista_archivos = []

"""| Comando para abrir un archivo gif |"""
def open_gif():
    rutas_gifs = filedialog.askopenfilenames(filetypes=[("GIF files", "*.gif")])
    if rutas_gifs:
        for ruta in rutas_gifs:
            a = showinfo(ruta, box1, [])
            show_gif(ruta,box2, window)
            Write_txt(ruta)
            lista_archivos.append(a[0])



def open_carpeta():
    seleccion = filedialog.askdirectory(title="Seleccione una carpeta") or filedialog.askopenfilenames(filetypes=[("GIF files", "*.gif")])
    if isinstance(seleccion, str) and os.path.isdir(seleccion):
        rutas_gifs = [os.path.join(seleccion, f) for f in os.listdir(seleccion) if f.lower().endswith(".gif")]
    else:  
        rutas_gifs = seleccion
    
    for ruta in rutas_gifs:
        a = showinfo(ruta, box1, [])
        show_gif(ruta, box2, window) 
        Write_txt(ruta)
        for i in range(len(a)):
            lista_archivos.append(a[i])

    
def show_history():
    with open("historial/rutas.txt", "r") as archivo:
        for linea in archivo:
            showinfo(linea.strip(), box1, [])
            show_gif(linea.strip(), box2, window)

"""| Ventana principal |"""
window = ctk.CTkToplevel() #Se crea la ventana
window.geometry("1550x850") #Se da el tamaño a la ventana
window.title("Extractor de Archivos GIF") #Se le asigna un nombre a la ventana
window.resizable(True, True)
window.grab_set() #Queda debajo de cualquier ventana que se abra
util_ventana.centrar_ventana(window, 1550, 870)
fondo = util_imagen.leer_imagen("./imagenes/imgfondo.jpg", (1960,1150))
background_label = ctk.CTkLabel(master=window, text="",image=fondo, width=0, height=0)
background_label.place(relx=0, rely=0, relwidth=1, relheight=1)




"""| Cajas de texto y Marco con Scrool |"""
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

def modificar():
    button_confirmar.configure(state="normal" )
    entry.configure(state="normal")
    combobox.configure(state="normal")
    entry_dato.configure(state="normal")

def confirmar():
    print(entry.get(), combobox.get())
    for i in range(len(lista_archivos)):
        print(i + 1, entry.get())
        if (str(i + 1) == str(entry.get())):
            box1.delete(1.0, "end")
            data_find = lista_archivos[i]
            data_find.change_dato(str(combobox.get()), str(entry_dato.get()))
            break

    for dats in lista_archivos:
        showinfo(dats.ruta, box1, [])
    
        

size = 16 #Tamaño original de las letras

box1 = ctk.CTkTextbox(master=window, wrap=ctk.NONE, font=("Times New Roman", size), width=300, height=760)
box1.place(x=10, y=10)

box2 = ctk.CTkScrollableFrame(master=window, width=350, height=750)
box2.place(x=1150, y=10)


box1.bind("<MouseWheel>", scrool)


"""| Botones |"""
botton_gif = ctk.CTkButton(master=window, text="ABRIR GIFs", command=open_gif)
botton_gif.place(x=350, y=20)

botton_folder = ctk.CTkButton(master=window, text="ABRIR CARPETAS de GIFs", command=open_carpeta)
botton_folder.place(x=550, y=20)


botton_save = ctk.CTkButton(master=window, text="ARCHIVOS GIFs ANTERIORES", command=show_history)    
botton_save.place(x=800, y=20)

button_modificate = ctk.CTkButton(master=window, text="MODIFICAR ARCHIVO", command=modificar)    
button_modificate.place(x=350, y=60)

# ingresa el numero que quiere modificar 
entry = ctk.CTkEntry(master=window, state="disable" )
entry.place(x=500, y=60)
# ingresa el dato a modificar

entry_dato = ctk.CTkEntry(master=window, state="disable" )
entry_dato.place(x=500, y=100)


opciones = ["archivo", "version", "tamaño","cantidad_colores", "comprension", "formato_numerico", "background", "date_creacion", "date_modificacion", "comentarios"]
combobox = ctk.CTkComboBox(master=window, values=opciones, state="disable" )
combobox.place(x=750, y=60)

button_confirmar = ctk.CTkButton(master=window, text="CONFIRMAR", state="disable", command=confirmar)
button_confirmar.place(x=1000, y=60)



window.bind("<Control-MouseWheel>", zoom)
window.mainloop() #Se inicializa la ventana 