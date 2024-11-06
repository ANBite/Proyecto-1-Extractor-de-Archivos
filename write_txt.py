class Write_txt():
    def __init__(self, ruta): 
        with open("historial/rutas.txt", "a") as archivo:
            archivo.write(str(ruta) + "\n")

