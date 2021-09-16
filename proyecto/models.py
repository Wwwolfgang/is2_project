from django.contrib.auth.models import Permission
from django.db import models
from django.utils import timezone
from sso.models import User
# Create your models here.
class RolProyecto(models.Model):
    """
    Model del rol de proyecto.
    Se almacena el nombre del rol, sus permisos, los participantes del proyecto que tienen el rol,
    y el proyecto al que pertenece dicho rol.
    """
    nombre = models.CharField(verbose_name='Nombre del rol', max_length=60, blank=False,null=False)
    permisos = models.ManyToManyField(Permission)
    participantes = models.ManyToManyField(User,blank=True,null=True)
    proyecto = models.ForeignKey('proyecto', on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        permissions = (
                    ('p_administrar_roles','Permite que el usuario pueda configurar, crear, importar y eliminar roles del proyecto. Solo los permisos del scrum master no se podrán modificar.'),
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
            ("p_acceder_proyectos","Permiso de acceder proyecto."),
            ("p_cancelar_proyectos","Permiso de cancelar proyecto."),
            ("p_editar_proyectos","Permiso de editar proyecto."),
            ("p_finalizar_proyectos","Permiso de finalizar proyecto."),      
        )

class UserStory(models.Model):
    """
    Clase user story
    TODO: Agregar el campo 'encargado', que relacione el user story con el participante del proyecto encargado de 
    realizar la tarea
    """
    nombre = models.CharField(verbose_name='Nombre del user story', max_length=20, blank=False,null=False)
    descripcion = models.CharField(verbose_name='Descripción del user story', max_length=60, blank=False,null=False)
    tiempoEstimado = models.PositiveIntegerField(blank=False)
    #encargado = 
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