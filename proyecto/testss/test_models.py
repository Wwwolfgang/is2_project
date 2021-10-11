from django.test import TestCase
from sso import models
from django.utils import timezone
from django.urls import reverse
from sso.forms import UpdateRolSistemaForm,UserAssignRolForm
from django.contrib.auth.models import Group,Permission
from django.test.client import Client, RequestFactory
from allauth.utils import get_user_model
import pytest
from guardian.shortcuts import assign_perm, remove_perm, get_user_perms
from pytest_django.asserts import assertTemplateUsed
from decimal import Decimal
from datetime import datetime, timedelta


from proyecto import views, models, forms

class TestModels(TestCase):
    def setUp(self):
        """ Setup de objetos de prueba """
        username="wolfgang" 
        first_name="Wolfgang"
        last_name="Wiens Wohlgemuth"
        email="wwwolfgang469@gmail.com"
        self.factory = RequestFactory()
        self.user = models.User.objects.create(username=username, first_name=first_name,last_name=last_name,email=email)
        self.user2 = models.User.objects.create(username='is1', first_name='IS1',last_name='Testuser',email='is2equipo15cuenta1@gmail.com')
        self.proyecto = models.Proyecto.objects.create(nombreProyecto='proyectotest',estado_de_proyecto='A')
        self.productBacklog = models.ProductBacklog.objects.create(proyecto=self.proyecto)


    def userstoryCreate(self,estado_ap='T',estado_user_story='TD'):
        self.userstory = models.UserStory.objects.create(nombre='Prueba',descripcion='Prueba',prioridad_user_story='B',estado_aprobacion=estado_ap,creador=self.user2,product_backlog=self.productBacklog,estado_user_story=estado_user_story)

    def test_creacion_historial(self):
        self.userstoryCreate()
        models.HistorialUS.objects.create(nombre=self.userstory.nombre,descripcion=self.userstory.descripcion,version=1,prioridad=self.userstory.prioridad_user_story,us_fk=self.userstory)
        self.assertTrue(models.HistorialUS.objects.exists())