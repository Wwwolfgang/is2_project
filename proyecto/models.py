from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.
class Proyecto(models.Model):
    """
    Clase proyecto

    TODO: Realizar user story para poder implementar en agregarSprintProyecto()
    y actualizarBurnDownChart()
    """
    nombreProyecto = models.CharField(max_length = 50)
    fechaInicio = datetime.date.today()
    fechaFin = datetime.date.today()
    codProyecto = 0
    estadoProyecto = 0
    nroSprints = 0

    # listaSprints = Sprint[]
    # listaUsuarios = Usuario[]
    # listaRoles = Rol[]

    def getNombreProyecto(self):
        return self.nombreProyecto

    def getFechaInicio(self):
        return self.fechaInicio

    def getEstadoProyecto(self):
        return self.estadoProyecto

    def setNombreProyecto(self, nombreProyecto):
        self.nombreProyecto = nombreProyecto

    def finalizarProyecto(self):
        print("Se finalizo el proyecto")

    def generarCodigoProyecto(self):
        print("Codigo generado")
        cod = 0
        return cod #Función para traer siguiente código integer de la BD

    def actualizarEstadoProyecto(self, estadoProyecto):
        self.estadoProyecto = estadoProyecto

    def setCodProyecto(self):
        self.codProyecto = generarCodigoProyecto()

    # def agregarSprintProyecto(self, sprintNuevo):
    # self.listaSprints.add(sprintNuevo)
    def obtenerCantidadSprints(self):
        return self.nroSprints

    def marcarSprintTerminado(self, codSprint):
        self.estadoProyecto = codSprint
    # def actualizarBurnDownChart(self, dificultad):
    # self