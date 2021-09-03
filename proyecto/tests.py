from proyecto.models import RolProyecto
from django.db.models import fields
from django.db.models.query_utils import PathInfo
from django.http import response
from django.test import TestCase
from sso.models import User
from django.urls import reverse
from django.contrib.auth.models import Group,Permission, User
from django.test.client import Client, RequestFactory
from allauth.utils import get_user_model
import pytest
from pytest_django.asserts import assertTemplateUsed

# Create your tests here.



@pytest.mark.django_db
class TestModelRolProyecto:
    """
    Pruebas unitarias que comprueban las funciones del model RolProyecto
    """

    def test_rolproyecto_lista_permisos(self):
        """
        Prueba unitaria que comprueba que la función get_permisos() retorne la lista de
        permisos esperada.
        """
        permisos = list(Permission.objects.all())
        rol = RolProyecto.objects.create(nombre='rol1')
        rol.permisos.set(permisos)
        rol.save()
        permisos_obtenidos = rol.get_permisos()

        assert permisos_obtenidos == permisos, "No se pudieron cargar los permisos"
    
    def test_rolproyecto_nombre_vacio(self):
        """
        Prueba unitaria que comprueba que el campo nombre de un rol tenga que ser
        distinto de ''
        """
        rol = RolProyecto.objects.create(nombre='rol2')

        assert rol.nombre != ''

@pytest.mark.django_db
class TestViewsRolProyecto(TestCase):
    def create_rol(self, name="Scrum Master"):
        return Group.objects.create(name=name)

    def user(self, username="wolfgang", first_name="Wolfgang", last_name="Wiens Wohlgemuth",email="wwwolfgang469@gmail.com"):
        return User.objects.create(username=username, first_name=first_name,last_name=last_name,email=email)

    def test_agregar_rol_proyecto_view(self):
        """
        Test encargado de comprobar que se cargue correctamente la página de agregar rol.
        """
        rol = self.create_rol()
        response = self.client.get(reverse('proyecto:agregar-rol',kwargs={'pk':rol.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
 