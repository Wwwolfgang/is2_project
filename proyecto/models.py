from django.contrib.auth.models import Permission
from django.db import models
from datetime import datetime
from django.db.models.base import Model

from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields.related import ManyToManyField
from sso.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class RolProyecto(models.Model):
    """
    Model del rol de proyecto.
    Se almacena el nombre del rol, sus permisos, los participantes del proyecto que tienen el rol,
    y el proyecto al que pertenece dicho rol.
    """
    nombre = models.CharField(verbose_name='Nombre del rol', max_length=60, blank=False,null=False)
    permisos = models.ManyToManyField(Permission)
    participantes = models.ManyToManyField(User,blank=True)
    proyecto = models.ForeignKey('proyecto', on_delete=models.CASCADE, blank=True, null=True)
    
    def get_permisos(self):
        """
        Función que retorna la lista de permisos asociados al rol
        """
        return [p for p in self.permisos.all()]
    
    def __str__(self):
       return self.nombre


class Proyecto(models.Model):
    """
    Clase proyecto
    El modelo todavía no está completo
    Por el momento se configura:

    - El nombre del Proyecto
    - La fecha de inicio del Proyecto
    - La fecha estimada de finalización del Proyecto
    - Un codigo del Proyecto
    - El numero de Sprints
    - La duración por default de un Sprint
    - El estado del proyecto siendo inicialmente Inicializado y después Activo, Finalizado o Cancelado
    - El equipo de participantes en el proyecto. 
    - TODO equipo de desarrolladores,etc
    
    También se definieron algunos permisos iniciales, cuya cantidad va aumentar. Estos permisos van a ser asignados al usuario por el proyecto.

    """
    nombreProyecto = models.CharField(max_length = 50)
    fechaInicio = models.DateField(null=False, blank=False, help_text="Fecha de inicialización del proyecto", default=datetime.now )
    fechaFin = models.DateField(null=False, blank=False, help_text="Fecha estimada de finalización del proyecto", default=datetime.now )
    ESTADO_DE_PROYECTO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inicializado'),
        ('C', 'Cancelado'),
        ('F', 'Finalizado'),
    ]
    estado_de_proyecto = models.CharField(
        max_length=1,
        choices=ESTADO_DE_PROYECTO_CHOICES,
        default='I',
    )
    owner = models.ForeignKey(User,blank=True,null=True,on_delete=CASCADE,related_name='creador')
    equipo = models.ManyToManyField(User,blank=True)
    equipo_desarrollador = models.ManyToManyField('proyectuser',blank=True)

    class Meta:
        permissions = (
            #Permisos de proyecto
            ("p_acceder_proyectos","Permiso de acceder proyecto."),
            ("p_cancelar_proyectos","Permiso de cancelar proyecto."),
            ("p_editar_proyectos","Permiso de editar proyecto."),
            ("p_finalizar_proyectos","Permiso de finalizar proyecto."),
            ("p_administrar_participantes","Permiso para agregar y eliminar participantes del proyecto."),
            #Permiso de roles
            ("p_administrar_roles","Permite que el usuario pueda agregar, editar, importar y eliminar roles del proyecto. Solo los permisos del scrum master no se podrán modificar."),
            #Permisos de sprint
            ("p_administrar_sprint","Permite que el usuario pueda gestionar los parámetros de los sprints, así como planificarlos, iniciarlos y finalizarlos."),
            #Permisos de user story
            #El permiso para administrar user stories va a ser aplicado junto al permiso de agregar y editar los dailys,
            ("p_administrar_us","Permite que el usuario pueda editar los user stories del proyecto (cambiar estado, nombre, descripción y horas)."),
            ("p_eliminar_us","Permite que el usuario pueda eliminar user stories del proyecto (cambiar estado, nombre, descripción y horas)."),
            ("p_administrar_us_qa","Con este permiso el usuario puede cambiar el estado de un user story a QA. Inicialmente es un permiso reservado al scrum master."),
            ("p_aprobar_us","Con este permiso el usuario puede agregar un user story en estado no aprobado, así como también modificarlo y aprobarlo para que pase al product backlog."),
            #Agregado un permiso para eliminar el daily, que se gestionará como un permiso adicional
            ("p_eliminar_daily","Permite que el usuario pueda eliminar el daily asociado a un user story."),
            ("p_administrar_devs","Con este permiso el usuario puede gestionar los desarrolladores en un sprint."),    
        )


class ProyectUser(models.Model):
    """ 
        Clase ProyctUser
        Es un usuario o desarrollador asignado a un sprint
        Se especifica el usuario y su carga horaria diaria y el sprint al cual fue asignado
    """
    usuario = models.ForeignKey(User,on_delete=CASCADE)
    horas_diarias = models.DecimalField(blank=False,decimal_places=2,max_digits=4,null=False,help_text='La cantidad de horas que trabaja el desarrollador por día.')
    sprint = models.ForeignKey('sprint', related_name='sprint_team',on_delete=CASCADE)

    def __str__(self):
       return "%s" % self.usuario.first_name + " " + self.usuario.last_name + "  " + str(self.horas_diarias) + " hs/D"


class ProductBacklog(models.Model):
    """ Clase de Product Backlog es una llave foranea al proyecto """
    proyecto = models.ForeignKey(Proyecto,on_delete=CASCADE)


class Sprint(models.Model):
    """ 
        Clase Sprint
        El sprint es la unidad que contiene un conjunto de user storys
        Campos:

        - Identificador o Nombre
        - Fecha inicio TODO falta asignar
        - Fecha fin TODO falta asignar
        - Duración del sprint en dias TODO falta hacer advertencias en la planificación
        - Estado del sprint
        - Carga horaria sumando los tiempos de los user storys
        - Proyecto al cual pertenece
        - Horas disponibles, que es el total de días por horas de desarrolladores disponibles
    """
    identificador = models.CharField(default='Sprint',max_length=50)
    fechaInicio = models.DateField(null=True)
    fechaFin = models.DateField(null=True,help_text='Fecha estimada de finalización del Sprint. Dependiendo de esta fecha se mostrarán alertas.')
    duracionSprint = models.IntegerField(null=False, blank=False, default=14,validators=[MinValueValidator(1),MaxValueValidator(60)], help_text="Duración estimada en días")
    ESTADO_DE_SPRINT_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inicializado'),
        ('C', 'Cancelado'),
        ('F', 'Finalizado'),
    ]
    estado_de_sprint = models.CharField(
        max_length=1,
        choices=ESTADO_DE_SPRINT_CHOICES,
        default='I',
    )
    carga_horaria = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=8,help_text="Total de horas de todos los user storys asignados",default=0)
    proyecto = models.ForeignKey(Proyecto,on_delete=CASCADE, null=True)
    horas_disponibles = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=8,default=0)

    def __str__(self):
       return self.identificador

       
class UserStory(models.Model):
    """
    Clase user story
    El modelo de user story es un modelo muy importante del sistema.
    Sus campos son:

    - Nombre
    - Descripción del user story
    - Tiempo de duración hasta completar estimado por el scrum master
    - Tiempo de duración hasta completar estimado por el encargado
    - Tiempo promedio calculado pro los dos tiempos anteriores
    - Prioridad del user story: baja, alta, media, emergencia
    - Estado de aprobación: temporal si fue creado pero no aprobado y aprobado si se aprobó y no puede ser modificado
    - Encargado, desarrollador asignado al user story
    - Creador, usuario que lo creó
    - Sprint, el sprint al cual el user story fue asignado
    - Product Backlog para hacer la relación al proyecto (Un campo un poco innecesario)
    - Un campo del último tiempo estimado. En caso de que el user story debe ser tratado en un sprint futuro.
    TODO 

    - agregar un campo que guarda las horas completadas en el sprint si es que el user story no fue terminado en un sprint.
    """
    nombre = models.CharField(verbose_name='Nombre del user story', max_length=100, blank=False,null=False)
    descripcion = models.TextField(verbose_name='Descripción del user story',blank=True)
    tiempo_estimado_scrum_master = models.PositiveIntegerField(blank=True,null=True,help_text="Tiempo de duración estimado por el scrum master.",default=0)
    tiempo_estimado_dev = models.PositiveIntegerField(blank=True,null=True,help_text="Tiempo de duración estimado por el desarrollador asignado.",default=0)
    tiempo_promedio_calculado = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=4,help_text="Tiempo de duración promedio entre los dos tiempos estimados.")
    PRIORIDAD_DE_USER_STORY_CHOICES = [
        ('B', 'Baja'),
        ('A', 'Alta'),
        ('M', 'Media'),
        ('E','Emergencia')
    ]
    prioridad_user_story = models.CharField(
        max_length=1,
        choices=PRIORIDAD_DE_USER_STORY_CHOICES,
        default='B',
    )
    ESTADO_APROBACION_USER_STORY = [
        ('T', 'Temporal'),
        ('A', 'Aprobado'),
        ('C', 'Cancelado'),
    ]
    estado_aprobacion = models.CharField(
        max_length=1,
        choices= ESTADO_APROBACION_USER_STORY,
        default='T',
    )
    ESTADO_DE_USER_STORY_CHOICES = [
        ('TD', 'To do'),
        ('DG', 'Doing'),
        ('DN', 'Done'),
        ('QA','Quality Assurance')
    ]
    estado_user_story = models.CharField(
        max_length=2,
        choices=ESTADO_DE_USER_STORY_CHOICES,
        default='TD',
    )
    last_estimated = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=4)
    encargado = models.ForeignKey(ProyectUser,blank=True,null=True,on_delete=CASCADE)
    creador = models.ForeignKey(User,blank=True,null=True,on_delete=CASCADE)
    sprint = models.ForeignKey('sprint',blank=True,null=True,on_delete=CASCADE)
    product_backlog = models.ForeignKey('productbacklog',on_delete=CASCADE, blank=True,null=True)

    class Meta:
        permissions = (
            ("us_manipular_userstory_dailys","Permiso de manipular los dailys de un userstory."),
        )


class HistorialUS(models.Model):
    """ 
    Modelo de historial. Cada entrada de historial es una nueva versión de un user story, es creado para cada modificación de un user story.
    Guarda:
    
    - El nombre del user story
    - La descripción del user story
    - El número de versión de historial
    - La prioridad del user story
    - El user story padre de las versiones
    """
    nombre = models.CharField(verbose_name='Nombre del user story', max_length=100, blank=False, null=False)
    descripcion = models.TextField(verbose_name='Descripción del user story', blank=True)
    version = models.IntegerField()
    PRIORIDAD_DE_USER_STORY_CHOICES = [
        ('B', 'Baja'),
        ('A', 'Alta'),
        ('M', 'Media'),
        ('E', 'Emergencia')
    ]
    prioridad = models.CharField(
        max_length=1,
        choices=PRIORIDAD_DE_USER_STORY_CHOICES,
        default='B',
    )
    us_fk = models.ForeignKey(UserStory, on_delete=CASCADE, null=False)
    log = models.TextField(verbose_name='Log en donde se almacenan los cambios de estado en el ciclo de vida del User Story', blank=True)

class Daily(models.Model):
    """
    Clase Daily: El desarrollador anota cuanto tiempo trabajó en el user story en horas. Puede anotar los impedimientos que encontró en el proceso y
    puede anotar los progresos que hizo. Cada objeto daily se relaciona con un sprint ya que un user story puede ser tratado en diferentes sprints si no fue
    terminado. Además se agrega la fecha de creación del daily.
    Campos:

    - duracipon en horas decimales
    - los impedimientos
    - los progresos
    - el user story padre
    - el sprint activo
    - la fecha de creación
    """
    duracion = models.DecimalField(help_text='Trabajo realizado en horas.', decimal_places=2, max_digits=4)
    impedimiento_comentario = models.TextField(verbose_name='Descripcion de las dificultades encontradas durante el desarrollo', blank=True)
    progreso_comentario = models.TextField(verbose_name='Descripcion de los progresos encontrados durante el desarrollo', blank=True)
    user_story = models.ForeignKey('userstory',on_delete=CASCADE, blank=True, null=True)
    sprint = models.ForeignKey('sprint', on_delete=CASCADE, blank=True,null=True)
    fecha = models.DateField(null=True,blank=True)

