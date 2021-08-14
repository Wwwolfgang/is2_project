import datetime
class comentario:
    codComentario = ""
    codUserStory = ""
    codProyecto = ""
    descripcion = ""
    fecha = datetime.date()
    def generarCodComentario():
        print("Se genero comentario")
    def obtenerCodUserStory(self):
        return self.codUserStory
    def obtenerCodProyecto(self):
        return self.codProyecto
    def obtenerDescripcion(self):
        return self.descripcion
    def modificarDescripcion(self,descripcion):
        self.descripcion=descripcion
    def marcarFechaComentario(self):
        self.fecha = datetime.date()
    #def usuarioComentando(self, codUsuario):
    #   self.codComentario = codComentario
    #   Que hace esta funcion?