from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField
class User(AbstractUser):
    """
    Esta clase es un usuario personalizado que hereda de la classe AbstractUser, diferente del usuario normal de Django.
    Esto será util para relacionar los usuarios con los roles de sistema y de proyecto.
    """
    is_administrator = models.BooleanField(verbose_name='Administrador',default=False)

    

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "users"

<<<<<<< Updated upstream

class RolSistema(models.Model):
    name = models.CharField(verbose_name='Nombre del Rol', max_length=50, blank=False,null=False,help_text='Define el nombre del Rol de sistema')
    permisos = models.ManyToManyField('permiso')

    class Meta:
        verbose_name_plural = "system_roles"


class Permiso(models.Model):
    name = CharField(max_length=150,unique=True)

    def __str__(self):
        return self.name
    class Meta: 
        verbose_name_plural = 'permisos'
=======
        permissions = [
            ('custom_acceder_ususario','Test de prueba')
        ]


>>>>>>> Stashed changes
