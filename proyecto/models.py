from django.contrib.postgres.fields import ArrayField
from django.db import models
from sso.models import User
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import Permission
from django.db import models
from django.utils import timezone
from sso.models import User

class comentario(models.Model):
    codComentario   = models.CharField(max_length=50)
    codUserStory    = models.CharField(max_length=50)
    codProyecto     = models.CharField(max_length=50)
    descripcion     = models.CharField(max_length=50)
    fecha           = models.DateField(datetime.date.today)
    def __str__(self):
        return self

class usuarioProyecto(models.Model):
    codProyecto     = models.CharField(max_length=50)
    rolUsuario      = models.CharField(max_length=50)
    def __str__(self):
        return self


class userStory(models.Model):
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


class RolProyecto(models.Model):
    nombre = models.CharField(verbose_name='Nombre del rol', max_length=60, blank=False,null=False)
    permisos = models.ManyToManyField(Permission)
    participantes = models.ManyToManyField(User,blank=True)
    proyecto = models.ForeignKey('proyecto', on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        permissions = (
                    ("p_administrar_roles","Permite que el usuario pueda configurar, crear, importar y eliminar roles del proyecto. Solo los permisos del scrum master no se podrán modificar."),
        )
    def get_permisos(self):
        return [p for p in self.permisos.all()]
    
    def __str__(self):
       return self.nombre


class Proyecto(models.Model):
    """
    Clase proyecto

    TODO: Realizar user story para poder implementar en agregarSprintProyecto()
    y actualizarBurnDownChart()
    """
    nombreProyecto = models.CharField(max_length = 50)
    fechaInicio = models.DateField(null=False, blank=False, help_text="Fecha de inicialización del proyecto", default=timezone.now)
    fechaFin = models.DateField(null=False, blank=False, help_text="Fecha estimada de finalización del proyecto", default=timezone.now)
    codProyecto = models.IntegerField()
    nroSprints = models.IntegerField()
    duracionSprint = models.IntegerField(null=False, blank=False, default=14, help_text="Duración de un Sprint")
    ESTADO_DE_PROYECTO_CHOICES = [
        ('A', 'Activo'),
        ('C', 'Cancelado'),
        ('F', 'Finalizado'),
    ]
    estado_de_proyecto = models.CharField(
        max_length=1,
        choices=ESTADO_DE_PROYECTO_CHOICES,
        default='A',
    )
    equipo = models.ManyToManyField(User)

    class Meta:
        permissions = (
            ("p_acceder_proyectos","Permiso de acceder proyecto."),
            ("p_cancelar_proyectos","Permiso de cancelar proyecto."),
            ("p_editar_proyectos","Permiso de editar proyecto."),
            ("p_finalizar_proyectos","Permiso de finalizar proyecto."),      
        )
