from django.contrib.postgres.fields import ArrayField
from django.db import models
from sso.models import User
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField

class comentario(models.Model):
    codComentario   = models.CharField(max_length=50)
    codUserStory    = models.CharField(max_length=50)
    codProyecto     = models.CharField(max_length=50)
    descripcion     = models.CharField(max_length=50)
    fecha           = models.DateField(datetime.date.today)
    def __str__(self):
        return self
    def modificarDescripcion(self,descripcion):
        self.descripcion=descripcion
    #def usuarioComentando(self, codUsuario):
    #   self.codComentario = codComentario
    #   Que hace esta funcion?
    pass

class usuarioProyecto(models.Model):
    codProyecto     = models.CharField(max_length=50)
    rolUsuario      = models.CharField(max_length=50)
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
        - Correcto funcionamiento de la clase para ser implementada en otros metodos
        - Adicion de datos relacionados a user story en postgresql para realizar tests
    """
    nombreUserStory     = models.CharField(max_length=50)
    codigoUserStory     = models.CharField(max_length=50)
    listaParticipantes  = models.ManyToManyField(User,related_name="participantes")
    descripcionUserStory= models.CharField(max_length=50)
    estado              = models.CharField(max_length=50)
    comentarios         = models.ManyToManyField(comentario,related_name="comentario")
    estimacion          = models.IntegerField()
    tiempoEmpleado      = models.IntegerField()
    def __str__(self):
        return self
    def modificarNombre(self, nombre):
        self.nombreUserStory = nombre
    def actualizarEstado(self, estado):
        self.estado = estado
    def actualizarDescripcion(self, descripcionUserStory):
        self.descripcionUserStory = descripcionUserStory
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
    nombreSprint    = models.CharField(max_length=50)
    codSprint       = models.CharField(max_length=50)
    nroUserStories  = models.IntegerField()
    listaStories    = ManyToManyField( userStory, max_length= 100 )
    fechaInicio     = models.DateField()
    fechaFin        = models.DateField()
    duracionSprint  = models.IntegerField()
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
    nombreRol       = models.CharField(max_length=50)
    claveProyecto   = models.CharField(max_length=50)
    permisos        = ArrayField(models.CharField(max_length=50))
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

class kanban(models.Model):
    columnas = models.ManyToManyField(userStory)
    def moverUserStory(codUserStory):
       print("Se movio el user story")
       return True
    def asignarUserStory( username ):
       print("Se agrego al user story")
    def actualizarKanban():
       print("Se actualizo el kanban")
    #def generarKanban(userStory[]):
    def generarKanban(listaStories):
       print("Se genero el kanban")

class historialCambiosUS(models.Model):
    codHistorialCambios = models.CharField(max_length=50)
    codUserStory        = models.CharField(max_length=50)
    codProyecto         = models.CharField(max_length=50)
    codUsuario          = models.CharField(max_length=50)
    descripcionCambio   = models.CharField(max_length=50)
    fecha               = models.DateTimeField()
    def generarCambio(self, descripcion, codProyecto, codUsuario, codUserStory):
        self.codUserStory = codUserStory
        self.codProyecto = codProyecto
        self.codUsuario = codUsuario
        self.descripcionCambio = descripcion
    def obtenerFecha(self):
        return self.fecha

class burnDownChart(models.Model):
    codBurnDownChart    = models.CharField(max_length=50)
    codSprintRel        = models.CharField(max_length=50)
    codProyRel          = models.CharField(max_length=50)
    datosTeoricos       = ArrayField(ArrayField(models.IntegerField()))
    datosReales         = ArrayField(ArrayField(models.IntegerField()),max_length=2)
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
    nombreProyecto  = models.CharField(max_length=50)
    fechaInicio     = models.DateTimeField()
    fechaFin        = models.DateTimeField()
    codProyecto     = models.CharField(max_length=50)
    estadoProyecto  = models.IntegerField()
    nroSprints      = models.IntegerField()
    listaSprints    = models.ManyToManyField(sprint)
    listaUsuarios   = models.ManyToManyField(User)
    listaRoles      = models.ManyToManyField(rol)
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