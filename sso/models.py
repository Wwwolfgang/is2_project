from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import datetime

from django.db.models.fields import CharField
class User(AbstractUser):
    """
    Esta clase es un usuario personalizado que hereda de la classe AbstractUser, diferente del usuario normal de Django.
    Esto será util para relacionar los usuarios con los roles de sistema y de proyecto.
    """
    is_administrator = models.BooleanField(verbose_name='Administrador',default=False)
    objects = UserManager()
    def __str__(self):
        return self.username

    class Meta:
        """ Listado inicial de permisos del sistema. Este listado a futuro va ser expandido y se podrá elegir más permisos. """
        verbose_name_plural = "users"

        permissions = [
            ('pg_is_user','El usuario es un usuario registrado que se le asignó un rol. Con este permiso tiene la posibilidad de ver más en el sistema.'),
            ('pg_puede_crear_proyecto','El usuario puede crear nuevos proyectos.'),
            ('pg_puede_acceder_proyecto','El usuario puede acceder los proyectos.')
        ]
