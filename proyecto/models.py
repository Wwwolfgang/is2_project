from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from sso.models import User
import datetime
# Create your models here.
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