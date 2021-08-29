from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

from django.db.models.fields import CharField
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

        permissions = [
            ('custom_acceder_ususario','Test de prueba'),
            ('custom_acceder_proyecto','Acceder proyectos'),

        ]
