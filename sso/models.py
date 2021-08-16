from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
class User(AbstractUser):
    """
    Esta clase es un usuario personalizado que hereda de la classe AbstractUser, diferente del usuario normal de Django.
    Esto será util para relacionar los usuarios con los roles de sistema y de proyecto.
    
    TODO
        - Agregar los campos restantes del modelo
    """
    #descripcion = models.TextField(max_length=500, blank=True, null=True)
    """Este es un campo de texto de prueba. A futuro será eliminado y se agregarán mas campos."""

    def __str__(self):
        return self.username

class usuario:
    username = ""
    tokenSesion = False
    direccionCorreo = ""
    def crearProyecto():
        print("El proyecto fue creado.\n")
    def iniciarSistema():
        print("El sistema fue inicializado.\n")
    def cerrarSesion():
        print("Se cerro la sesion.\n")

class usuarioProyecto:
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


class userStory:
    """ 
    Clase user story

    TODO
        - Correcto funcionamiento de la clase para ser implementada en otros metodos
        - Adicion de datos relacionados a user story en postgresql para realizar tests
    """
    def __init__(self,nombreUserStory,codigoUserStory,listaParticipantes,descripcionUserStory,estado,comentarios,estimacion,tiempoEmpleado):
        self.nombreUserStory = nombreUserStory
        self.codigoUserStory = codigoUserStory
        self.listaParticipantes = listaParticipantes
        self.descripcionUserStory = descripcionUserStory
        self.estado = estado
        self.comentarios = comentarios
        self.estimacion = estimacion
        self.tiempoEmpleado = tiempoEmpleado
    def __str__(self):
        return self
    def obtenerNombre(self):
        return self.nombreUserStory
    def modificarNombre(self, nombre):
        self.nombreUserStory = nombre
    def actualizarEstado(self, estado):
        self.estado = estado
    def actualizarDescripcion(self, descripcionUserStory):
        self.descipcionUserStory = descripcionUserStory
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

class sprint:
    """ 
    Clase sprint

    TODO
        - Desarrollar user story
    """
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

class rol:
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

class historialCambiosUS:
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

class comentario:
    #codComentario = ""
    #codUserStory = ""
    #codProyecto = ""
    #descripcion = ""
    #fecha = datetime.date.today()
    def __init__(self,codComentario,codUserStory,codProyecto,descripcion,fecha):
        self.codComentario = codComentario
        self.codUserStory = codUserStory
        self.codProyecto = codProyecto
        self.descripcion = descripcion
        self.fecha = fecha
    def __str__(self):
        return self
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
        self.fecha = datetime.date.today()
    #def usuarioComentando(self, codUsuario):
    #   self.codComentario = codComentario
    #   Que hace esta funcion?

class burnDownChart:
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
