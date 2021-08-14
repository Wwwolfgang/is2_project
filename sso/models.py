from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Esta clase es un usuario personalizado que hereda de la classe AbstractUser, diferente del usuario normal de Django.
    Esto será util para relacionar los usuarios con los roles de sistema y de proyecto.
    
    #TODO
    
    - Agregar los campos restantes del modelo
    """
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    """Este es un campo de texto de prueba. A futuro será eliminado y se agregarán mas campos."""

    def __str__(self):
        return self.username