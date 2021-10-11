from proyecto.models import Proyecto, RolProyecto, Sprint, UserStory, Daily, ProyectUser
from sso import models
from django.db.models import fields
from django.db.models.query_utils import PathInfo
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group,Permission
from django.test.client import Client, RequestFactory
from allauth.utils import get_user_model
from datetime import datetime
import pytest
from pytest_django.asserts import assertTemplateUsed
from datetime import datetime
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

@pytest.fixture
def proyecto_creado():
    nombreProyecto = 'Proyecto 1'
    fechaInicio = datetime.now()
    fechaFin = datetime.now()
    estado_de_proyecto = 'I'
    return Proyecto.objects.create(nombreProyecto = nombreProyecto,fechaInicio = fechaInicio,fechaFin = fechaFin, estado_de_proyecto = estado_de_proyecto)

@pytest.fixture
def user_story_creado():
    nombre = "User Story"
    descripcion = "Descripcion de User Story"
    tiempo_estimado_scrum_master = 14
    tiempo_estimado_dev = 14
    prioridad_user_story = 'B'
    estado_aprobacion = 'T'
    estado_user_story = 'TD'
    return UserStory.objects.create(nombre = nombre, descripcion = descripcion, tiempo_estimado_scrum_master = tiempo_estimado_scrum_master, tiempo_estimado_dev = tiempo_estimado_dev, prioridad_user_story = prioridad_user_story, estado_aprobacion = estado_aprobacion, estado_user_story = estado_user_story )

@pytest.fixture
def daily_creado():
    duracion = 15
    impedimiento_comentario = "Impedimiento1\nImpedimiento2\nImpedimiento3"
    progreso_comentario = "Progreso1\nProgreso2\nProgreso3"
    fecha = datetime.now()
    return Daily.objects.create(duracion = duracion, impedimiento_comentario = impedimiento_comentario, progreso_comentario = progreso_comentario, fecha = fecha)

@pytest.fixture
def proyecto_user_creado(): 
    horas_diarias = 9
    return ProyectUser.objects.create(horas_diarias = horas_diarias)

@pytest.fixture
def sprint_creado():
    identificador = 'Sprint'
    fechaInicio = datetime.now()
    fechaFin = datetime.now()
    duracionSprint = 15
    estado_de_sprint = 'A'
    sprint = Sprint.objects.create(identificador = identificador, fechaInicio = fechaInicio, fechaFin = fechaFin,duracionSprint = duracionSprint, estado_de_sprint= estado_de_sprint)
    return sprint

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
    TODO: Atributo 'client' no existe, reemplazar por atributo parecido o agregar en la clase
    """
    @pytest.fixture
    def cliente_loggeado(self, usuario_creado):
        client = Client()
        client.login(username='user_test', password='password123')
        return client
    def rol_proyecto(self):
        rol = RolProyecto.objects.create(nombre='roltest')
        rol.permisos.set(list(Permission.objects.all().filter(codename__startswith='p_')))
        rol.save()
        return rol

    def test_editar_rol_proyecto_view(self, cliente_loggeado):
        """
        Test encargado de comprobar que se cargue correctamente la página de editar rol.
        """
        rolproyecto = self.rol_proyecto()
        client = cliente_loggeado
        proyecto = Proyecto.objects.create(nombreProyecto='proyectotest')
        response = client.get(reverse('proyecto:rol-editar',kwargs={'pk_proy':proyecto.pk,'id_rol':rolproyecto.id}), follow=True)
        assert response.status_code == 403

    def test_lista_rol_proyecto_view(self, cliente_loggeado,proyecto_creado):
        """
        Test encargado de comprobar que se cargue correctamente la página de listar roles.
        """
        proyecto = proyecto_creado
        proyecto.owner = cliente_loggeado
        client = cliente_loggeado
        response = client.get(reverse('proyecto:roles',kwargs={'pk_proy':proyecto.pk}),follow=True)
        assert response.status_code == 200

    def test_agregar_rol_proyecto_view(self, proyecto_creado, cliente_loggeado):
        """
        Test encargado de comprobar que se cargue correctamente la página de agregar rol.
        """
        client = cliente_loggeado
        proyecto = proyecto_creado
        response = client.get(reverse('proyecto:agregar-rol',kwargs={'pk_proy':proyecto.pk}), follow=True)
        assert response.status_code == 200

    def test_importar_rol_proyecto_view(self, proyecto_creado, cliente_loggeado):
        """
        Test encargado de comprobar que se cargue correctamente la página de agregar rol.
        """
        client = cliente_loggeado
        proyecto = proyecto_creado
        response = client.get(reverse('proyecto:importar-roles',kwargs={'pk_proy':proyecto.pk}), follow=True)
        assert response.status_code == 200

@pytest.mark.django_db
class TestModelsProyecto:
    """
    Tests para comprobar las funcionalidades del modelo de proyecto
    """
    def test_proyecto_nombre_vacio(self,proyecto_creado):
        proyectoTest = proyecto_creado
        assert proyectoTest.nombreProyecto != ''
    
    def test_proyecto_fecha_invalida(self,proyecto_creado):
        proyectoTest = proyecto_creado
        assert abs( proyectoTest.fechaFin - proyectoTest.fechaInicio ) == proyectoTest.fechaFin - proyectoTest.fechaInicio, "Error: Fecha Final es mas reciente que Fecha Inicial"
    
    def test_proyecto_owner_(self,proyecto_creado,usuario_creado):
        proyectoTest = proyecto_creado
        userTest = usuario_creado
        proyectoTest.save()
        userTest.save()
        proyectoTest.owner = userTest
        assert '@' in proyectoTest.owner.email 
    

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
        assert response.status_code == 200

@pytest.mark.django_db
class TestModelSprint:
    """
    Pruebas unitarias que comprueban las funciones del model Sprint

    """
    def test_model_sprint(self):
        sprint = Sprint.objects.create(fechaInicio=datetime.now(), fechaFin=datetime.now(), estado_de_sprint='A')
        estado_sprint = Sprint.objects.get(pk =sprint.pk)
        self.assertEqual(estado_sprint.estado_de_sprint,'A')

    def test_fechaInicio(self):
        """
        Prueba unitaria que comprueba que el campo nombre de un rol tenga que ser
        distinto de ''
        """
        sprint = Sprint.objects.create(fechaInicio=datetime.now(), fechaFin=datetime.now(), estado_de_sprint='A')
        assert abs(sprint.fechaFin - sprint.fechaInicio) == sprint.fechaFin - sprint.fechaInicio, "Error: Fecha Final es mas reciente que Fecha Inicial"
    
@pytest.mark.django_db
class TestViewsProyectoUser:
    """
    Tests para comprobar las funcionalidades de los views de proyecto user
    """
    def proyecto_user_inicializado(self,proyecto_user_creado):
        proyectoUser = proyecto_user_creado
        proyectoUser.permisos.set(list(Permission.objects.all()))
        proyectoUser.save()
        return proyectoUser

@pytest.mark.django_db
class TestModelsUserStory:
    """
    Tests para comprobar las funcionalidades de los modelos de User Story
    """
    def test_user_story_nombre_invalido(self,user_story_creado):
        user_story = user_story_creado
        nombre = user_story.nombre
        caracteresInvalidos = "0123456789!@#$%^&*()_+-=[]<>?/"
        for caracter in caracteresInvalidos:
            assert caracter not in nombre
    def test_user_story_descripcion_vacia(self,user_story_creado):
        user_story = user_story_creado
        descripcion = user_story.descripcion
        assert descripcion != ''
    def test_user_story_tiempo_estimado_invalido(self,user_story_creado):
        user_story = user_story_creado
        tiempo_scrum = user_story.tiempo_estimado_scrum_master
        tiempo_dev = user_story.tiempo_estimado_dev
        assert tiempo_scrum > 0 and tiempo_scrum < 60 and tiempo_dev > 0 and tiempo_dev < 60
    def test_user_story_prioridad_invalida(self,user_story_creado):
        user_story = user_story_creado
        prioridad = user_story.prioridad_user_story
        assert prioridad in user_story.PRIORIDAD_DE_USER_STORY_CHOICES[0]
    def test_user_story_estado_invalido(self,user_story_creado):
        user_story = user_story_creado
        estado_aprobacion = user_story.estado_aprobacion
        estado_user_story = user_story.estado_user_story
        assert estado_aprobacion in user_story.ESTADO_APROBACION_USER_STORY[0] and estado_user_story in user_story.ESTADO_DE_USER_STORY_CHOICES[0]
    def test_user_story_creador(self,user_story_creado,usuario_creado):
        user_story = user_story_creado
        creador = usuario_creado
        user_story.save()
        creador.save()
        user_story.creador = creador
        assert '@' in user_story.creador.email

@pytest.mark.django_db
class TestModelsDaily:
    """
    Test para comprobar las funcionalidades de los modelos de Daily
    """
    def test_daily_duracion_invalida(self,daily_creado):
        """
        La duracion del daily no puede durar mas de 60 minutos
        """
        daily = daily_creado
        assert daily.duracion > 0 and daily.duracion < 60
    def test_daily_lista_impedimiento_invalida(self,daily_creado):
        daily = daily_creado
        assert len(daily.impedimiento_comentario) > 5
    def test_daily_lista_progreso_invalida(self,daily_creado):
        daily = daily_creado
        assert len(daily.progreso_comentario) > 5
    def test_daily_user_story(self,daily_creado,user_story_creado):
        daily = daily_creado
        user_story = user_story_creado
        daily.save()
        user_story.save()
        daily.user_story = user_story
        assert daily.user_story.estado_aprobacion == 'T'

@pytest.mark.django_db
class TestViewsDaily:
    @pytest.fixture
    def cliente_loggeado(self, usuario_creado):
        client = Client()
        client.login(username='user_test', password='password123')
        return client
    def test_agregar_daily_view(self,daily_creado,user_story_creado,sprint_creado,proyecto_creado,cliente_loggeado):
        daily = daily_creado
        user_story = user_story_creado
        sprint = sprint_creado
        client = cliente_loggeado
        proyecto = proyecto_creado
        daily.save()
        user_story.save()
        daily.user_story = user_story
        response = client.get(reverse('proyecto:userstory-add-daily',kwargs={'pk_proy':proyecto.pk,'sprint_id':sprint.pk, 'us_id':user_story.pk}))
        assert response.status_code == 200
    def test_editar_daily_view(self,daily_creado,user_story_creado,sprint_creado,proyecto_creado,cliente_loggeado):
        daily = daily_creado
        user_story = user_story_creado
        sprint = sprint_creado
        client = cliente_loggeado
        proyecto = proyecto_creado
        daily.save()
        user_story.save()
        daily.user_story = user_story
        response = client.get(reverse('proyecto:editar-daily',kwargs={'pk_proy':proyecto.pk,'sprint_id':sprint.pk, 'us_id':user_story.pk, 'd_pk':daily.pk}))
        assert response.status_code == 200
    def test_eliminar_daily_view(self,daily_creado,user_story_creado,sprint_creado,proyecto_creado,cliente_loggeado):
        daily = daily_creado
        user_story = user_story_creado
        sprint = sprint_creado
        proyecto = proyecto_creado
        client = cliente_loggeado
        daily.save()
        user_story.save()
        daily.user_story = user_story
        response = client.get(reverse('proyecto:eliminar-daily',kwargs={'pk_proy':proyecto.pk,'sprint_id':sprint.pk, 'us_id':user_story.pk, 'd_pk':daily.pk}))
        assert response.status_code == 200
    
@pytest.mark.django_db
class TestViewSprints:

    """
    Test para comprobar la funcionalidad de los views de Sprints
    """

    def sprint_inicializado(self):
        sprint = sprint_creado()
        return sprint

    @pytest.fixture
    def cliente_loggeado(self, usuario_creado):
        client = Client()
        client.login(username='user_test', password='password123')
        return client


    def test_lista_sprint_view(self, cliente_loggeado, usuario_creado):
        """
        Test encargado de comprobar que se cargue correctamente la página de listar Sprints.
        """
        response = cliente_loggeado.get(reverse('proyecto:index'), follow=True)
        assert response.status_code == 200


    def test_sprint_update_view(self, cliente_loggeado, usuario_creado):
        """
        Test para comprobar la edición de un sprint
        """
        sprint = self.sprint_inicializado()
        proyecto = Proyecto.objects.create(nombreProyecto='proyectotest')
        response = self.client.get(
            reverse('proyecto:sprint-edit', kwargs={'pk_proy': proyecto.pk, 'sprint_id': sprint.pk}), follow=True)
        assert response.status_code == 403
