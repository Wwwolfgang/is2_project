from proyecto.models import Proyecto, RolProyecto
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
    def rol_proyecto(self):
        rol = RolProyecto.objects.create(nombre='roltest')
        rol.permisos.set(list(Permission.objects.all().filter(codename__startswith='p_')))
        rol.save()
        return rol

    def test_editar_rol_proyecto_view(self):
        """
        Test encargado de comprobar que se cargue correctamente la página de editar rol.
        """
        rolproyecto = self.rol_proyecto()
        proyecto = Proyecto.objects.create(nombreProyecto='proyectotest')
        print(rolproyecto)
        response = self.client.get(reverse('proyecto:rol-editar',kwargs={'pk_proy':proyecto.pk,'id_rol':rolproyecto.id}), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_lista_rol_proyecto_view(self):
        """
        Test encargado de comprobar que se cargue correctamente la página de listar roles.
        """
        proyecto = Proyecto.objects.create(nombreProyecto='proyectotest')
        response = self.client.get(reverse('proyecto:roles',kwargs={'pk_proy':proyecto.pk}),follow=True)
        self.assertEqual(response.status_code, 200)
 