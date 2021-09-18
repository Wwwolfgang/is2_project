from proyecto.models import Proyecto, RolProyecto
from sso import models
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
@pytest.fixture
def create_rol(self, name="Scrum Master"):
    return Group.objects.create(name=name)

@pytest.fixture
def usuario_creado():
    username="wolfgang" 
    first_name="Wolfgang"
    last_name="Wiens Wohlgemuth"
    email="wwwolfgang469@gmail.com"
    return models.User.objects.create(username=username, first_name=first_name,last_name=last_name,email=email)
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
class TestViewsRolProyecto:
    """
    Tests para comprobar las funcionalidades de los views de rol proyecto
    """
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
        response = self.client.get(reverse('proyecto:rol-editar',kwargs={'pk_proy':proyecto.pk,'id_rol':rolproyecto.id}), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_lista_rol_proyecto_view(self):
        """
        Test encargado de comprobar que se cargue correctamente la página de listar roles.
        """
        proyecto = Proyecto.objects.create(nombreProyecto='proyectotest')
        response = self.client.get(reverse('proyecto:roles',kwargs={'pk_proy':proyecto.pk}),follow=True)
        self.assertEqual(response.status_code, 200)

    def test_agregar_rol_proyecto_view(self):
        """
        Test encargado de comprobar que se cargue correctamente la página de agregar rol.
        """
        proyecto = Proyecto.objects.create(nombreProyecto='proyectotest')
        response = self.client.get(reverse('proyecto:agregar-rol',kwargs={'pk_proy':proyecto.pk}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_importar_rol_proyecto_view(self):
        """
        Test encargado de comprobar que se cargue correctamente la página de agregar rol.
        """
        proyecto = Proyecto.objects.create(nombreProyecto='proyectotest')
        response = self.client.get(reverse('proyecto:importar-roles',kwargs={'pk_proy':proyecto.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
@pytest.mark.django_db
class TestViewsProyecto:
    """
    Tests para comprobar las funcionalidades de los views de proyecto
    """
    @pytest.fixture
    def cliente_loggeado(self, usuario_creado):
        client = Client()
        client.login(username='user_test', password='password123')
        return client

    def test_lista_proyecto_view(self, cliente_loggeado, usuario_creado):
        """
        Test encargado de comprobar que se cargue correctamente la página de listar proyectos.
        """
        response = cliente_loggeado.get(reverse('proyecto:index'), follow=True)
        self.assertEqual(response.status_code, 200)
    
 
