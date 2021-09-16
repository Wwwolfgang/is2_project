from django.contrib.auth.models import Permission
from django.db import models
from datetime import datetime
from django.db.models.base import Model

from django.db.models.deletion import CASCADE
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
    class Meta:
        permissions = (
                    ("p_administrar_roles","Permite que el usuario pueda configurar, crear, importar y eliminar roles del proyecto. Solo los permisos del scrum master no se podrán modificar."),
        )

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
            ("p_acceder_proyectos","Permiso de acceder proyecto."),
            ("p_cancelar_proyectos","Permiso de cancelar proyecto."),
            ("p_editar_proyectos","Permiso de editar proyecto."),
            ("p_finalizar_proyectos","Permiso de finalizar proyecto."),      
        )


class ProyectUser(models.Model):
    usuario = models.ForeignKey(User,on_delete=CASCADE)
    horas_diarias = models.DecimalField(blank=False,decimal_places=2,max_digits=4,null=False,help_text='La cantidad de horas que trabaja el desarrollador por día.')
    sprint = models.ForeignKey('sprint', related_name='sprint_team',on_delete=CASCADE)


class Sprint(models.Model):
    identificador = models.CharField(default='Sprint',max_length=50)
    fechaInicio = models.DateField(null=True)
    fechaFin = models.DateField(help_text='Fecha estimada de finalización del Sprint. Dependiendo de esta fecha se mostrarán alertas.')
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
    proyecto = models.ForeignKey(Proyecto,on_delete=CASCADE, null=True)

    def __str__(self):
       return self.identificador
