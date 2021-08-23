from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField

class comentario(models.Model):
    codComentario = models.CharField(max_length=50)
    codUserStory = models.CharField(max_length=50)
    codProyecto = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    fecha = models.DateField(datetime.date.today)
    def __str__(self):
        return self
    def modificarDescripcion(self,descripcion):
        self.descripcion=descripcion
    #def usuarioComentando(self, codUsuario):
    #   self.codComentario = codComentario
    #   Que hace esta funcion?
    pass

class usuario(models.Model):
    username = ""
    tokenSesion = False
    direccionCorreo = ""
    def crearProyecto():
        print("El proyecto fue creado.\n")
    def iniciarSistema():
        print("El sistema fue inicializado.\n")
    def cerrarSesion():
        print("Se cerro la sesion.\n")

class usuarioProyecto(models.Model):
    codProyecto = ""
    rolUsuario = ""
    def cambiarRol(self, username):
        self.rolUsuario = username #?
    def solicitarCambioRol(self):
        if( self.rolUsuario == 1 ):
            return True
        return False
    def agregarUsuarioProyecto():
        print("Se agrego el usuario al proyecto")
    def asignarUserStory(self,codUserStory, username):
        print("Se ha asignado el usuario al user story")
    def crearRolProyecto(self,codProyecto, listaPermisos, descripcion):
        print("Se creo el rol")
    def crearUserStory(nombreUserStory, descripcionUserStory):
        print("El user story fue creado")
    def cambiarUserStory( descripcionUserStory ):
        print("El user story fue cambiado")
    def modificarEstadoUserStory(codUserStory, estado):
        print("El user story fue modificado")
    def crearSprint(nombreSprint, duracionSprint):
        print("El sprint fue creado")


class userStory(models.Model):
    """ 
    Clase user story

    TODO
        -Vinculacion de la clase comentario con la clase userStory
    """
    
    nombreUserStory = models.CharField(max_length=50)
    codigoUserStory = models.CharField(max_length=50)
    listaParticipantes = ArrayField(models.CharField(max_length=50),max_length=10)
    descripcionUserStory = models.CharField(max_length=50)
    estado = models.CharField(max_length=10)
    comentarios = ManyToManyField( comentario, related_name="comentario" )
    estimacion = models.IntegerField()
    tiempoEmpleado = models.IntegerField()
    def __str__(self):
        return self
    def modificarNombre(self, nombre):
        self.nombreUserStory = nombre
    def actualizarEstado(self, estado):
        self.estado = estado
    def actualizarDescripcion(self, descripcionUserStory):
        self.descripcionUserStory = descripcionUserStory
    def agregarParticipantes(self, participante):       #Se utiliza userStory.objects.aggregate()
        self.listaParticipantes.append(participante)
        self.listaParticipantes.sort
    def eliminarParticipantes(self, participante):
        posicion = 0
        for i in self.listaParticipantes:
            if( participante.__eq__(i) ):
                self.listaParticipantes.pop(posicion)
                return True
            posicion = posicion + 1
        return False
    def mostrarParticipantes(self):
        for participante in self.listaParticipantes:
            print(participante)
    def actualizarHistorial():
        print("Se actualizo el historial")
    def generarEstimacion(int,int2):
        print("Se estima que el user story dure 1 mes")

class sprint(models.Model):
    """ 
    Clase sprint

    TODO
        - Vinculacion de la clase user story con la clase sprint
        - Desarrollar sprint
    """
    nombreSprint = models.CharField(max_length=50)
    codSprint = models.CharField(max_length=50)
    nroUserStories = models.IntegerField()
    listaStories = ManyToManyField( userStory, max_length= 100 )
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    duracionSprint = 0
    def modificarNombreSprint(self,nombreSprint):
        self.nombreSprint = nombreSprint
    def agregarUserStory(self, nuevoUserStory):
       self.listaStories.append(nuevoUserStory)
       self.listaStories.sort
       self.nroUserStories = self.nroUserStories + 1
    def eliminarUserStory(self, codigoUserStory):
        posicion = 0
        for userStory in self.listaStories:
            if( userStory.codigoUserStory.__eq__(codigoUserStory) ):
                self.listaStories.pop(posicion)
            posicion = posicion + 1
    def actualizarFechaInicio(self):
        self.fechaInicio = datetime.date.today
    def actualizarFechaFin(self):
        self.fechaFin = datetime.date.today
    def terminarSprint():
        print("Se termino el sprint")
    def generarCodigoSprint(self):
        print("Se genero un codigo")
    def ingresarDuracionSprint(self,duracion):
        self.duracionSprint = duracion
    def actualizarDuracionSprint(self,duracion):
        print("Se actualizo la duracion de sprint")

class rol(models.Model):
    nombreRol = ""
    claveProyecto = ""
    permisos = [""]
    def modificarRol(self, nombreRol, permisos):
        self.nombreRol = nombreRol
        self.permisos = permisos
        print("Se modifico el rol")
    def obtenerNombreRol(self):
        return self.nombreRol
    def obtenerPermisos(self):
        return self.permisos
    def obtenerClave(self):
        return self.claveProyecto

#class kanban:
    #columnas = userStory[]
    #def moverUserStory(userStory codUserStory):
    #   print("Se movio el user story")
    #   return True
    #def asignarUserStory( username ):
    #   print("Se agrego al user story")
    #def actualizarKanban():
    #   print("Se actualizo el kanban")
    #def generarKanban(userStory[]):
    #def generarKanban(userStory listaStories):
    #   print("Se genero el kanban")

class historialCambiosUS(models.Model):
    codHistorialCambios = ""
    codUserStory = ""
    codProyecto = ""
    codUsuario = ""
    descripcionCambio = ""
    fecha = datetime.date.today
    def generarCambio(self, descripcion, codProyecto, codUsuario, codUserStory):
        self.codUserStory = codUserStory
        self.codProyecto = codProyecto
        self.codUsuario = codUsuario
        self.descripcionCambio = descripcion
    def obtenerFecha(self):
        return self.fecha

class burnDownChart(models.Model):
    codBurnDownChart = ""
    codSprintRel = ""
    codProyRel = ""
    datosTeoricos = [0][0]
    datosReales = [2][0]
    def crearLineaTeorica( dificultadEstimadaTotal, totalDias ):
        print("Se creo la linea teorica")
    def actualizarLineaReal( storyPointsCompletado, dia ):
        print("Se actualizo la linea real")
    def dibujarBurnDownChart():
        print("Se dibujo el burn down chart")
    def borrarBurnDownChart():
        print("Se borro el burn down chart")



class proyecto:
    """ 
    Clase proyecto
    
    TODO: Realizar user story para poder implementar en agregarSprintProyecto()
    y actualizarBurnDownChart()
    """
    nombreProyecto = ""
    fechaInicio = datetime.date.today
    fechaFin = datetime.date.today
    codProyecto = ""
    estadoProyecto = 0
    nroSprints = 0
    #listaSprints = Sprint[]
    #listaUsuarios = Usuario[]
    #listaRoles = Rol[]
    def obtenerNombreProyecto(self):
        return self.nombreProyecto
    def obtenerFechaInicio(self):
        return self.fechaInicio
    def obtenerEstadoProyecto(self):
        return self.estadoProyecto
    def ingresarNombreProyecto(self, nombreProyecto ):
        self.nombreProyecto = nombreProyecto
    def finalizarProyecto(self):
        print("Se finalizo el proyecto")
    def generarCodigoProyecto(self):
        print("Codigo generado")
    def actualizarEstadoProyecto(self, estadoProyecto ):
        self.estadoProyecto = estadoProyecto
    #def agregarSprintProyecto(self, sprintNuevo):
        #self.listaSprints.add(sprintNuevo)
    def obtenerCantidadSprints(self):
        return self.nroSprints
    def marcarSprintTerminado(self, codSprint):
        self.estadoProyecto = codSprint
    #def actualizarBurnDownChart(self, dificultad):
        #self