class Datos():
    def __init__(self, archivo, version, tamanio, cantcolores, comprension, formatonum, backgroudn, nimagenes, creacin, modificnacion, comentarios, ruta):
        self.archivo = archivo
        self.version = version
        self.tamanio = tamanio
        self.cantcolores = cantcolores
        self.comprension = comprension
        self.formatonum = formatonum
        self.backgroudn = backgroudn
        self.nimagenes = nimagenes
        self.creacion = creacin
        self.modificacion = modificnacion
        self.comentarios = comentarios
        self.ruta = ruta

    def change_dato(self, type:str, data):
        if type == "archivo":
            self.archivo = data
        elif type == "version":
            self.version = data
        elif type == "tamaño":
            self.tamanio = data
        elif type == "cantidad_colores":
            self.cantcolores = data
        elif type == "comprension": 
            self.comprension = data
        elif type == "formato_numerico":
            self.formatonum = data
        elif type == "background":
            self.backgroudn = data
        elif type == "date_creacion": 
            self.creacion = data
        elif type == "date_modificacion":
            self.modificacion = data
        elif type == "comentarios":
            self.comentarios = data
    



    def return_ruta(self):
        return self.ruta

    def return_all_data(self):
        return 