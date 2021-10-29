from statistics import mode
from django.db.models import fields
from django.db.models.query_utils import PathInfo
from django.forms.forms import Form
from django.http import response
from django.shortcuts import get_object_or_404
from django.test import TestCase
import proyecto
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
from workalendar.america import Paraguay


from proyecto import views, models, forms

class SprintTest(TestCase):
    def setUp(self):
        """ Setup de objetos de prueba """
        username="wolfgang" 
        first_name="Wolfgang"
        last_name="Wiens Wohlgemuth"
        email="wwwolfgang469@gmail.com"
        self.factory = RequestFactory()
        self.user = models.User.objects.create(username=username, first_name=first_name,last_name=last_name,email=email)
        self.user2 = models.User.objects.create(username='is1', first_name='IS1',last_name='Testuser',email='is2equipo15cuenta1@gmail.com')
        self.proyecto = models.Proyecto.objects.create(nombreProyecto='proyectotest',estado_de_proyecto='A',owner=self.user2)
        self.productBacklog = models.ProductBacklog.objects.create(proyecto=self.proyecto)
        self.rol = models.RolProyecto.objects.create(nombre='Rol',proyecto=self.proyecto)

    def sprintCreate(self,estado = 'I',carga_horaria=0.0):
        """ Setup de un sprint de prueba """
        cal = Paraguay()
        self.sprint = models.Sprint.objects.create(identificador='Sprint 1',estado_de_sprint=estado,proyecto=self.proyecto,duracionSprint=14,carga_horaria=carga_horaria,fechaInicio=datetime.now(),fechaFin= cal.add_working_days(datetime.now(), 14))
        self.dev = models.ProyectUser.objects.create(usuario=self.user,horas_diarias=10,sprint=self.sprint)
    
    def userstoryCreate(self,estado_ap='T',estado_user_story='TD',encargado=None):
        self.userstory = models.UserStory.objects.create(nombre='Prueba',descripcion='Prueba',prioridad_user_story='B',estado_aprobacion=estado_ap,creador=self.user2,product_backlog=self.productBacklog,estado_user_story=estado_user_story,encargado=encargado)

    def dailyCreate(self):
        self.daily = models.Daily.objects.create(duracion=1.2,impedimiento_comentario='No funcionan los tests',progreso_comentario='Pude avanzar bien',user_story=self.userstory,sprint=self.sprint,fecha=datetime.now())

    def test_eliminar_rol_proyecto_view(self):
        """ Test para probar si el view EliminarRolProyectoView es alcanzable con los correctos kwargs y permisos """
        kwargs = {'pk_proy':self.proyecto.pk,'pk': self.rol.pk}
        url = reverse('proyecto:rol-eliminar', kwargs=kwargs)
        request = self.factory.get(url)
        request.user = self.user

        perm = Permission.objects.get(codename='p_administrar_roles')
        assign_perm(perm,request.user,self.proyecto)

        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,request.user,self.proyecto)

        response = views.EliminarRolProyectoView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)
        

    def test_lista_rol_proyecto_view(self):
        """ Test para probar si el view ListaRolProyectoView es alcanzable con los correctos kwargs y permisos """
        kwargs = {'pk_proy':self.proyecto.pk}
        url = reverse('proyecto:roles', kwargs=kwargs)
        request = self.factory.get(url)
        request.user = self.user

        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,request.user,self.proyecto)

        response = views.ListaRolProyectoView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_importar_rol_view(self):
        """ Test para probar si el view ImportarRolView es alcanzable con los correctos kwargs y permisos """
        kwargs = {'pk_proy':self.proyecto.pk}
        url = reverse('proyecto:importar-roles', kwargs=kwargs)
        perm = Permission.objects.get(codename='p_administrar_roles')
        request = self.factory.get(url)
        request.user = self.user
        assign_perm(perm,request.user,self.proyecto)

        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,request.user,self.proyecto)

        response = views.ImportarRolView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_assign_user_rolproyecto_view(self):
        """ Test para probar si el view AssignUserRolProyecto es alcanzable con los correctos kwargs y permisos """
        kwargs = {'pk_proy':self.proyecto.pk,'id_rol':self.rol.pk}
        url = reverse('proyecto:rol-assignar', kwargs=kwargs)
        perm = Permission.objects.get(codename='p_administrar_roles')
        request = self.factory.get(url)
        request.user = self.user
        assign_perm(perm,request.user,self.proyecto)
        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,request.user,self.proyecto)
        response = views.AssignUserRolProyecto.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_lista_proyectos_view(self):
        """ Test para probar si el view ListaProyectos es alcanzable con los correctos kwargs y permisos """
        url = reverse('proyecto:index')
        perm1 = Permission.objects.get(codename='pg_puede_acceder_proyecto')
        perm2 = Permission.objects.get(codename='pg_is_user')

        request = self.factory.get(url)
        request.user = self.user
        assign_perm(perm1,request.user)
        assign_perm(perm2,request.user)
        response = views.ListaProyectos.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_lista_proyectos_cancelados_view(self):
        """ Test para probar si el view ListaProyectosCancelados es alcanzable con los correctos kwargs y permisos """
        url = reverse('proyecto:cancelados')
        perm1 = Permission.objects.get(codename='pg_puede_acceder_proyecto')
        perm2 = Permission.objects.get(codename='pg_is_user')

        request = self.factory.get(url)
        request.user = self.user
        assign_perm(perm1,request.user)
        assign_perm(perm2,request.user)
        response = views.ListaProyectosCancelados.as_view()(request)
        self.assertEqual(response.status_code, 200)

    # def test_proyecto_detail_view(self):
    #     """ Test para probar si el view ProyectoDetailView es alcanzable con los correctos kwargs y permisos """
    #     kwargs = {'pk':self.proyecto.pk}
    #     url = reverse('proyecto:detail', kwargs=kwargs)
    #     perm = Permission.objects.get(codename='p_acceder_proyecto')

    #     request = self.factory.get(url)
    #     request.user = self.user
    #     assign_perm(perm,self.user,self.proyecto)

    #     response = views.ProyectoDetailView.as_view()(request,**kwargs)
    #     self.assertEqual(response.status_code, 200)

    def test_crear_proyecto_view(self):
        """ Test para probar si el view CreateProyectoView es alcanzable con los correctos kwargs y permisos """
        url = reverse('proyecto:create')
        perm = Permission.objects.get(codename='pg_puede_crear_proyecto')
        request = self.factory.get(url)
        request.user = self.user
        assign_perm(perm,request.user)
        response = views.CreateProyectoView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_agregar_participante_proyecto_view(self):
        """ Test para probar si el view AgregarParticipanteProyecto es alcanzable con los correctos kwargs y permisos """
        kwargs = {'pk_proy':self.proyecto.pk}
        url = reverse('proyecto:agregar-participantes-proyecto', kwargs=kwargs)
        perm = Permission.objects.get(codename='p_administrar_participantes')
        request = self.factory.get(url)
        request.user = self.user
        assign_perm(perm,request.user,self.proyecto)
        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,request.user,self.proyecto)
        response = views.AgregarParticipanteProyecto.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_solicitar_permisos_view(self):
        """ Test para probar si el view SolicitarPermisosView es alcanzable con los correctos kwargs y permisos """
        kwargs = {'pk_proy':self.proyecto.pk}
        url = reverse('proyecto:solicitud-permisos-proyecto', kwargs=kwargs)
        request = self.factory.get(url)
        request.user = self.user
        response = views.SolicitarPermisosView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_sprint_creation_view(self):
        """ Test para probar si el view AgregarSprintView es alcanzable con los correctos kwargs y permisos """
        kwargs = {'pk_proy': self.proyecto.pk}
        url = reverse('proyecto:agregar-sprint', kwargs=kwargs)
        request = self.factory.get(url)
        request.user = self.user
        perm = Permission.objects.get(codename='p_administrar_sprint')
        assign_perm(perm,request.user,self.proyecto)
        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,request.user,self.proyecto)
        response = views.AgregarSprintView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_sprint_creation_form(self):
        kwargs = {'pk_proy': self.proyecto.pk}
        form = forms.SprintCrearForm(data={'duracionSprint':15})
        self.assertTrue(form.is_valid())

    def test_sprint_equipo_view(self):
        """ Test para probar si el view EquipoSprintUpdateView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate()
        kwargs = {'pk_proy': self.proyecto.pk, 'pk': self.sprint.pk}
        url = reverse('proyecto:sprint-team-edit', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_administrar_devs')
        assign_perm(perm,self.user,self.proyecto)
        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)
        
        request = self.factory.get(url)
        request.user = self.user
        response = views.EquipoSprintUpdateView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)
        
        self.client.force_login(self.user)
        # r = self.client.post(url,data={'usuario':self.user2,'horas_diarias':7.5})
        # assert models.ProyectUser.objects.exists()
        # self.assertEqual(302, r.status_code)
        # teammember = models.ProyectUser.objects.create(usuario=self.user2,horas_diarias=7.5,sprint=self.sprint)
        # request = self.factory.post(url,data={'usuario':teammember.usuario,'horas_diarias':teammember.horas_diarias})
        # request.user = self.user
        # response = views.EquipoSprintUpdateView.as_view()(request,**kwargs)
        # self.assertEqual(response.status_code, 200)

    def test_sprint_update_view(self):
        """ Test para probar si el view SprintUpdateView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate()
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk}
        url = reverse('proyecto:sprint-edit', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_administrar_sprint')
        assign_perm(perm,self.user,self.proyecto)
        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)
        request = self.factory.get(url)
        request.user = self.user
        response = views.SprintUpdateView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_sprint_view(self):
        """ Test para probar si el view SprintView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate()
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk}
        url = reverse('proyecto:sprint-detail', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)
        request = self.factory.get(url)
        request.user = self.user
        response = views.SprintView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_product_backlog_view(self):
        """ Test para probar si el view ProductBacklog es alcanzable con los correctos kwargs y permisos """
        kwargs = {'pk_proy': self.proyecto.pk}
        url = reverse('proyecto:product-backlog', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_acceder_proyecto')

        assign_perm(perm,self.user,self.proyecto)

        request = self.factory.get(url)
        request.user = self.user
        response = views.ProductBacklogView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)
    
    def test_aprobar_userstory_view(self):
        """ Test para probar si el view AprobarUserStoryView es alcanzable con los correctos kwargs y permisos """
        self.userstoryCreate()
        kwargs = {'pk_proy': self.proyecto.pk, 'us_id': self.userstory.pk}
        url = reverse('proyecto:aprobar-user-story', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_aprobar_us')
        assign_perm(perm,self.user,self.proyecto)

        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)

        request = self.factory.get(url)
        request.user = self.user
        response = views.AprobarUserStoryView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_user_story_detail_view(self):
        self.sprintCreate()
        self.userstoryCreate()
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk, 'us_id': self.userstory.pk}
        url = reverse('proyecto:user-story-detail', kwargs=kwargs)

        request = self.factory.get(url)
        request.user = self.user
        response = views.UserStoryDetailView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_inspect_userstory_view(self):
        self.userstoryCreate()
        kwargs = {'pk_proy': self.proyecto.pk, 'us_id': self.userstory.pk}
        url = reverse('proyecto:user-story-detail-unassigned', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)

        perm = Permission.objects.get(codename='p_aprobar_us')
        assign_perm(perm,self.user,self.proyecto)

        request = self.factory.get(url)
        request.user = self.user
        response = views.InspectUserStoryView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    # def test_quitar_user_story_view(self):
    #     self.sprintCreate('I',15)
    #     teammember = models.ProyectUser.objects.create(usuario=self.user2,horas_diarias=7.5,sprint=self.sprint)
    #     self.userstoryCreate('A','TD',teammember)
    #     kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk, 'us_id': self.userstory.pk}
    #     url = reverse('proyecto:user-story-quitar', kwargs=kwargs)

    #     perm1 = Permission.objects.get(codename='p_administrar_us')
    #     perm2 = Permission.objects.get(codename='p_administrar_sprint')

    #     assign_perm(perm1,self.user,self.proyecto)
    #     assign_perm(perm2,self.user,self.proyecto)

    #     request = self.factory.get(url)
    #     request.user = self.user
    #     response = views.quitar_user_story_view(request,pk_proy=kwargs['pk_proy'],sprint_id=self.sprint.pk, us_id=self.userstory.pk)
    #     self.assertEqual(response.status_code, 200)

    # def test_iniciar_sprint_view(self):
    #     self.sprintCreate('I',15)
    #     kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk}
    #     url = reverse('proyecto:sprint-iniciar', kwargs=kwargs)

    #     perm = Permission.objects.get(codename='p_administrar_sprint')

    #     assign_perm(perm,self.user,self.proyecto)

    #     request = self.factory.get(url)
    #     request.user = self.user
    #     response = views.iniciar_sprint_view(request,pk_proy=kwargs['pk_proy'],sprint_id=self.sprint.pk)
    #     self.assertEqual(response.status_code, 200)

    def test_sprint_kanban_view(self):
        """ Test para probar si el view SprintKanbanView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate()
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk}
        url = reverse('proyecto:sprint-kanban', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)
        perm = Permission.objects.get(codename='p_aprobar_us')
        assign_perm(perm,self.user,self.proyecto)

        request = self.factory.get(url)
        request.user = self.user
        response = views.SprintKanbanView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_finalizar_sprint_view(self):
        """ Test para probar si el view FinalizarSprintView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate('A')
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk}
        url = reverse('proyecto:sprint-finalizar', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_administrar_sprint')
        assign_perm(perm,self.user,self.proyecto)
        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)
        request = self.factory.get(url)
        request.user = self.user
        response = views.FinalizarSprintView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_qa_view(self):
        """ Test para probar si el view QaView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate('A')
        self.userstoryCreate('A','QA')
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk, 'us_id':self.userstory.pk}
        url = reverse('proyecto:user-story-qa', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_administrar_us_qa')
        assign_perm(perm,self.user,self.proyecto)
        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)
        request = self.factory.get(url)
        request.user = self.user
        response = views.QaView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_finalizar_proyecto_view(self):
        """ Test para probar si el view FinalizarProyectoView es alcanzable con los correctos kwargs y permisos """
        kwargs = {'pk_proy': self.proyecto.pk}
        url = reverse('proyecto:finalizar-proyecto', kwargs=kwargs)

        perm = Permission.objects.get(codename='p_finalizar_proyectos')
        assign_perm(perm,self.user,self.proyecto)

        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)

        request = self.factory.get(url)
        request.user = self.user
        response = views.FinalizarProyectoView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_sprint_burndownchart_view(self):
        """ Test para probar si el view SprintBurndownchartView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate('A',13.5)
        kwargs = {'pk_proy': self.proyecto.pk ,'sprint_id': self.sprint.pk}
        url = reverse('proyecto:sprint-burndownchart', kwargs=kwargs)
        #Por algún motivo se queda congelado cuando le pongo las líneas de abajo
        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,self.user,self.proyecto)

        request = self.factory.get(url)
        request.user = self.user
        response = views.SprintBurndownchartView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_edit_daily_view(self):
        """ Test para probar si el view EditDailyView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate('A')
        self.userstoryCreate('A','DG')
        self.dailyCreate()
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk, 'us_id':self.userstory.pk, 'd_pk':self.daily.pk}
        url = reverse('proyecto:editar-daily', kwargs=kwargs)

        request = self.factory.get(url)
        request.user = self.user

        perm = Permission.objects.get(codename='us_manipular_userstory_dailys')
        assign_perm(perm,request.user,self.userstory)

        perm = Permission.objects.get(codename='p_administrar_us')
        assign_perm(perm,request.user,self.proyecto)
        
        perm = Permission.objects.get(codename='p_acceder_proyecto')
        assign_perm(perm,request.user,self.proyecto)

        response = views.EditDailyView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_eliminar_daily_view(self):
        """ Test para probar si el view EditDailyView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate('A')
        self.userstoryCreate('A','DG')
        self.dailyCreate()
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk, 'us_id':self.userstory.pk, 'd_pk':self.daily.pk}
        url = reverse('proyecto:eliminar-daily', kwargs=kwargs)

        perm = Permission.objects.get(codename='us_manipular_userstory_dailys')
        assign_perm(perm,self.user,self.userstory)
        request = self.factory.get(url)
        request.user = self.user
        response = views.EliminarDailyView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_reasignar_desarrrollador_view(self):
        """ Test para probar si el view ReasignarDesarrrolladorView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate('A')
        self.userstoryCreate('A','DG')
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk, 'us_id':self.userstory.pk}
        url = reverse('proyecto:user-story-reasignar', kwargs=kwargs)

        perm = Permission.objects.get(codename='us_manipular_userstory_dailys')
        assign_perm(perm,self.user,self.userstory)
        request = self.factory.get(url)
        request.user = self.user
        response = views.ReasignarDesarrrolladorView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)

    def test_intercambiar_dev_view(self):
        """ Test para probar si el view ReasignarDesarrrolladorView es alcanzable con los correctos kwargs y permisos """
        self.sprintCreate('A')
        kwargs = {'pk_proy': self.proyecto.pk, 'sprint_id': self.sprint.pk, 'dev_id':self.dev.pk}
        url = reverse('proyecto:sprint-dev-exchange', kwargs=kwargs)

        # perm = Permission.objects.get(codename='us_manipular_userstory_dailys')
        # assign_perm(perm,self.user,self.userstory)
        request = self.factory.get(url)
        request.user = self.user
        response = views.IntercambiarDevView.as_view()(request,**kwargs)
        self.assertEqual(response.status_code, 200)