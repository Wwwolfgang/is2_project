from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from sso.models import User
import datetime
# Create your models here.
class RolProyecto(models.Model):
    nombre = models.CharField(verbose_name='Nombre del rol', max_length=60, blank=False,null=False,unique=True)
    #Aquí debe ir un campo que mantenga el proyecto al que pertenece el rol
    permisos = models.ManyToManyField(Permission)
    def __str__(self):
       return self.nombre
    class Meta:
        permissions = (("p_administrar_sprints","Permite que el usuario pueda crear, configurar y borrar los sprints del proyecto. Además tendrá la capacidad de alargar y de terminar el sprint en cualquier momento. Podrá también planificar un nuevo sprint."),
                    ("p_administrar_user_stories","Con este permiso el usuario podrá crear nuevos user stories y podrá modificar los user stories."),
                    ("p_administrar_roles","Permite que el usuario pueda configurar, crear, importar y eliminar roles del proyecto. Solo los permisos del scrum master no se podrán modificar."),
                    ("p_administrar_usuarios","Puede asignar nuevos usuarios al proyecto o darles de baja."),
                    ("stakeholder","El usuario podrá ver los sprints, el Kanban y los user storys pero no podrá cambiar algo."),
        )
        
class Proyecto(models.Model):
    """
    Clase proyecto

    TODO: Realizar user story para poder implementar en agregarSprintProyecto()
    y actualizarBurnDownChart()
    """
    nombreProyecto = models.CharField(max_length = 50)
    fechaInicio = models.DateField(null=False, blank=False, help_text="Fecha de inicialización del proyecto", default=timezone.now())
    fechaFin = models.DateField(null=False, blank=False, help_text="Fecha estimada de finalización del proyecto", default=timezone.now())
    codProyecto = 0
    nroSprints = 0
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
            ("p_crear_proyecto","Permiso de crear nuevos proyectos."),
            ("p_acceder_proyectos","Permiso de acceder proyectos."),
                    
        )