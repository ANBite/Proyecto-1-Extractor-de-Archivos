import os
from tkinter import Label
from PIL import Image, ImageTk

def show_gif(ruta_gif, lugar_gif, ventana):
    gif = Image.open(ruta_gif) #Se obtiene el gif
    frames = [] #Lista para guardar los GIFs
    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))
    except EOFError:
        pass


    gif_label = Label(lugar_gif)
    gif_label.pack(padx=5, pady=5)

    def actualizar_frame(index):
        frame = frames[index]
        gif_label.config(image=frame)
        gif_label.image = frame
        ventana.after(100, actualizar_frame, (index + 1) % len(frames))
    
    if frames:
        actualizar_frame(0)
        