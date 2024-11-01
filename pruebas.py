import os
import time
from tkinter import filedialog, Text
import customtkinter as ctk

def obtener_info_gif(ruta_gif):
    try:
        with open(ruta_gif, 'rb') as f:
            # Código para obtener información del GIF como antes
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
                elif byte == b'\x2c' or byte == b'\x3b':
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

# Función para mostrar la información en la interfaz con colores
def mostrar_info(ruta, info):
    info_textbox.insert("end", f"Archivo: {ruta}\n", "titulo")
    for clave, valor in info.items():
        info_textbox.insert("end", f"{clave}: ", "clave")
        info_textbox.insert("end", f"{valor}\n", "valor")
    info_textbox.insert("end", "\n" + "-"*50 + "\n")

# Configuración de la interfaz gráfica
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Lector de GIFs (Bytes)")
ventana.geometry("600x500")

boton_abrir = ctk.CTkButton(ventana, text="Abrir GIFs", command=abrir_gifs)
boton_abrir.pack(pady=20)

# Usar Text en lugar de CTkTextbox
info_textbox = Text(ventana, width=70, height=20)
info_textbox.tag_configure("titulo", foreground="blue", font=("Helvetica", 10, "bold"))
info_textbox.tag_configure("clave", foreground="green")
info_textbox.tag_configure("valor", foreground="black")
info_textbox.pack(pady=20)

ventana.mainloop()
