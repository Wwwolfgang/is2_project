from typing import Reversible
import pytest
from proyecto.models import RolProyecto
from django.contrib.auth.models import Permission
from http import HTTPStatus
from sso.models import User
from django.test import Client
import unittest


# Create your tests here.


@pytest.fixture
def usuario():
    user = User(is_administrator=True)
    user.save()
    return user
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
class TestViewsRolProyecto(unittest.TestCase):
    def setUp(self):
        """
        Setear cliente
        """
        self.client = Client()

    def test_agregar_rol_proyecto_view(self):
        """
        Test encargado de comprobar que no ocurra nigun error al cargar la pagina con un usuario que ha iniciado sesion.
        """
        response = self.client.get('proyecto/<int:pk_proy>/rol/agregar')
        self.assertEqual(response.status_code, 200)
 