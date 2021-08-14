import datetime
class sprint:
    nombreSprint = ""
    codSprint = ""
    nroUserStories = 0
    #listaStories = userStory[]
    fechaInicio = datetime.date()
    fechaFin = datetime.date()
    duracionSprint = 0
    def modificarNombreSprint(self,nombreSprint):
        self.nombreSprint = nombreSprint
    #def agregarUserStory(self, nuevoUserStory):
    #   self.listaStories.append(nuevoUserStory)
    #   self.nroUserStories = self.nroUserStories + 1
    #def eliminarUserStory(self, codUserStory):
    #    if( codUserStory == self.listaStories ):
    #       eliminar()
    def actualizarFechaInicio(self):
        self.fechaInicio = datetime.date()
    def actualizarFechaFin(self):
        self.fechaFin = datetime.date()
    def terminarSprint():
        print("Se termino el sprint")
    def generarCodigoSprint(self):
        print("Se genero un codigo")
    def ingresarDuracionSprint(self,duracion):
        self.duracionSprint = duracion
    def actualizarDuracionSprint(self,duracion):
        print("Se actualizo la duracion de sprint")
        