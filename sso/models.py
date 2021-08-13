from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    descripcion = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.username