from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
class User(AbstractUser):
    """
    Esta clase es un usuario personalizado que hereda de la classe AbstractUser, diferente del usuario normal de Django.
    Esto será util para relacionar los usuarios con los roles de sistema y de proyecto.
    
    #TODO
    
    - Agregar los campos restantes del modelo
    """
    #descripcion = models.TextField(max_length=500, blank=True, null=True)
    """Este es un campo de texto de prueba. A futuro será eliminado y se agregarán mas campos."""

    def __str__(self):
        return self.username
class comentario(models.Model):
    codComentario = models.CharField(max_length=50)
    codUserStory = models.CharField(max_length=50)
    codProyecto = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    fecha = models.DateField(datetime.date.today())
    def __str__(self):
        return self
    def generarCodComentario():
        print("Se genero comentario")
    def obtenerCodComentario(self):
        return self.codComentario
    def obtenerCodUserStory(self):
        return self.codUserStory
    def obtenerCodProyecto(self):
        return self.codProyecto
    def obtenerDescripcion(self):
        return self.descripcion
    def obtenerFecha(self):
        return self.fecha
    def modificarDescripcion(self,descripcion):
        self.descripcion=descripcion
    def marcarFechaComentario(self):
        self.fecha = datetime.date.today()
    #def usuarioComentando(self, codUsuario):
    #   self.codComentario = codComentario
    #   Que hace esta funcion?

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

'''Clase user story
    #TODO: 
    *)Correcto funcionamiento de la clase para ser implementada en otros
    metodos
    *)Adicion de datos relacionados a user story en postgresql para realizar
    tests
'''
class userStory(models.Model):
    #def __init__(self,nombreUserStory,codigoUserStory,listaParticipantes,descripcionUserStory,estado,comentarios,estimacion,tiempoEmpleado):
    nombreUserStory = models.CharField(max_length=50)
    codigoUserStory = models.CharField(max_length=50)
    listaParticipantes = ArrayField(models.CharField(max_length=10))
    descripcionUserStory = models.CharField(max_length=50)
    estado = models.IntegerField()
    comentarios = models.ManyToManyField(comentario(codComentario = "",codUserStory = "",codProyecto = "",descripcion = "",fecha = datetime.date.today()))
    estimacion = models.IntegerField()
    tiempoEmpleado = models.IntegerField()
    def __str__(self):
        return self
    def obtenerNombreUserStory(self):
        return self.nombreUserStory
    def obtenerCodigoUserStory(self):
        return self.codigoUserStory
    def obtenerListaParticipantes(self):
        return self.listaParticipantes
    def obtenerDescripcionUserStory(self):
        return self.descripcionUserStory
    def obtenerEstado(self):
        return self.estado
    def obtenerComentarios(self):
        return self.comentarios
    def obtenerEstimacion(self):
        return self.estimacion
    def obtenerTiempoEmpleado(self):
        return self.tiempoEmpleado
    def modificarNombre(self, nombre):
        self.nombreUserStory = nombre
    def actualizarEstado(self, estado):
        self.estado = estado
    def actualizarDescripcion(self, descripcionUserStory):
        self.descripcionUserStory = descripcionUserStory
    def agregarParticipantes(self, participante):
        self.listaParticipantes.append(participante)
    def eliminarParpassicipantes(self, participante):
        for i in self.listaParticipantes:
            if( i == participante ):
                self.listaParticipantes.remove(participante)
                return True
        return False
    def actualizarHistorial():
        print("Se actualizo el historial")
    def generarEstimacion(int,int2):
        print("Se estima que el user story dure 1 mes")

'''Clase sprint
    #TODO: Desarrollar user story
'''
class sprint(models.Model):
    nombreSprint = ""
    codSprint = ""
    nroUserStories = 0
    #listaStories = userStory[]
    fechaInicio = datetime.date.today()
    fechaFin = datetime.date.today()
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
        self.fechaInicio = datetime.date.today()
    def actualizarFechaFin(self):
        self.fechaFin = datetime.date.today()
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

'''Clase kanban
    #TODO: Inutilizable sin user story
'''
#class kanban(models.Model):
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
    fecha = datetime.date.today()
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


'''Clase proyecto
    #TODO: Realizar user story para poder implementar en agregarSprintProyecto()
    y actualizarBurnDownChart()
'''
class proyecto(models.Model):
    nombreProyecto = ""
    fechaInicio = datetime.date.today()
    fechaFin = datetime.date.today()
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