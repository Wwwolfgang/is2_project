from statistics import mode
from django.db.models import fields
from django.db.models.query_utils import PathInfo
from django.forms.forms import Form
from django.http import response
from django.shortcuts import get_object_or_404
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
from datetime import date, datetime, timedelta


from proyecto import views, models, forms

class FormTest(TestCase):
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

    def sprintCreate(self,estado = 'I',carga_horaria=0.0):
        """ Setup de un sprint de prueba """
        self.sprint = models.Sprint.objects.create(identificador='Sprint 1',estado_de_sprint=estado,proyecto=self.proyecto,duracionSprint=14,carga_horaria=carga_horaria,fechaInicio=datetime.now())
    
    def userstoryCreate(self,estado_ap='T',estado_user_story='TD'):
        self.userstory = models.UserStory.objects.create(nombre='Prueba',descripcion='Prueba',prioridad_user_story='B',estado_aprobacion=estado_ap,creador=self.user2,product_backlog=self.productBacklog,estado_user_story=estado_user_story)

    def dailyCreate(self):
        self.daily = models.Daily.objects.create(duracion=1.2,impedimiento_comentario='No funcionan los tests',progreso_comentario='Pude avanzar bien',user_story=self.userstory,sprint=self.sprint,fecha=datetime.now())

    # def test_dev_crear_form(self):
    #     proyecto = models.Proyecto.objects.create(nombreProyecto='proyectotest',estado_de_proyecto='A')
    #     form = forms.DesarrolladorCreateForm(data={'usuario':self.user2,'horas_diarias':7.5},proyecto=proyecto.pk)
    #     self.assertTrue(form.is_valid())

    # def test_agregar_participante_form(self):
    #     form = forms.AgregarParticipanteForm(data={'equipo':self.user2},instance=self.proyecto,kwargs={'instance':self.proyecto.pk})
    #     self.assertTrue(form.is_valid())

    def test_permiso_solicitud_form(self):
        """ Test para probar el form con sus campos """
        form = forms.PermisoSolicitudForm(data={'asunto':'Solicitud','body':'Por favor mas permisos'})
        self.assertTrue(form.is_valid())

    def test_sprint_creation_form(self):
        """ Test para probar el form con sus campos """
        kwargs = {'pk_proy': self.proyecto.pk}
        form = forms.SprintCrearForm(data={'duracionSprint':15})
        self.assertTrue(form.is_valid())

    def test_sprint_modificar_form(self):
        """ Test para probar el form con sus campos """
        self.sprintCreate()
        form = forms.SprintModificarForm(data={'duracionSprint':17}, instance=self.sprint)
        self.assertTrue(form.is_valid())

    def test_sprint_finalizar_form(self):
        """ Test para probar el form con sus campos """
        self.sprintCreate()
        form = forms.SprintFinalizarForm(data={'estado_de_sprint':'F'}, instance=self.sprint)
        self.assertTrue(form.is_valid())

    def test_userstory_aprobar_form(self):
        """ Test para probar el form con sus campos """
        self.userstoryCreate()
        form = forms.UserstoryAprobarForm(data={'estado_aprobacion':'A'}, instance=self.userstory)
        self.assertTrue(form.is_valid())

    def test_userstory_agregar_form(self):
        """ Test para probar el form con sus campos """
        form = forms.AgregarUserStoryForm(data={'nombre':'Prueba','descripcion':'Prueba','prioridad_user_story':'B',})
        self.assertTrue(form.is_valid())

    def test_finalizar_proyecto_form(self):
        """ Test para probar el form con sus campos """
        form = forms.ProyectoFinalizarForm(data={'estado_de_proyecto':'F'},instance=self.proyecto)
        self.assertTrue(form.is_valid())
    
    def test_proyecto_edit_form(self):
        """ Test para probar el form con sus campos """
        form = forms.ProyectoEditForm(data={'nombreProyecto':'F','fechaInicio': datetime.now(),'fechaFin': datetime.now()+timedelta(days=20)},instance=self.proyecto)
        self.assertTrue(form.is_valid())

    def test_agregar_rol_proyecto(self):
        """ Test para probar el form con sus campos """
        form = forms.AgregarRolProyectoForm(data={'nombre':'Rol','permisos': get_object_or_404(Permission,codename='p_administrar_sprint')})
        self.assertTrue(form.errors['permisos'])
    
    def test_userstory_dev_form(self):
        """ Test para probar el form con sus campos """
        self.userstoryCreate()
        form = forms.UserStoryDevForm(data={'tiempo_estimado_dev':10,},instance=self.userstory)
        self.assertTrue(form.is_valid())

    def test_qa_form(self):
        """ Test para probar el form con sus campos """
        form = forms.QaForm(data={'comentario':'Aprobado'})
        self.assertTrue(form.is_valid())

    def test_daily_crear_form(self):
        """ Test para probar el form con sus campos """
        form = forms.DailyForm(data={'duracion':1.2,'impedimiento_comentario':'Ningún problema','progreso_comentario':'Avanzé bastante'})
        self.assertTrue(not form.is_valid())

    def test_daily_editar_form(self):
        """ Test para probar el form con sus campos """
        self.sprintCreate()
        self.userstoryCreate()
        self.dailyCreate()
        form = forms.DailyForm(data={'duracion':1.2,'impedimiento_comentario':'Ningún problema','progreso_comentario':'Avanzé bastante'},instance=self.daily)
        self.assertTrue(not form.is_valid())
