from . import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from proyecto.views import agregar_rol_proyecto_view
from django.urls import path
from django.views.generic import TemplateView
from .views import EliminarRolProyectoView, ProyectoDetailView,agregar_user_story_view, edit, cancelar, editar_rol_proyecto_view, ListaProyectos, AssignUserRolProyecto,ImportarRolView,iniciar_proyecto,cancelar_proyecto, CreateProyectoView
from .views import finalizar_proyecto, AgregarParticipanteProyecto, eliminarParticipanteView, AgregarDesarrolladorView,EditDesarrolladorView,EliminarDesarrolladorView,SolicitarPermisosView,AgregarSprintView,EquipoSprintUpdateView
from .views import UserStoryUdateView,SprintView,ListaProyectosCancelados, UserStoryDetailView, InspectUserStoryView, quitar_user_story_view, iniciar_sprint_view, SprintKanbanView,SprintUpdateView, mark_us_doing, mark_us_todo, mark_us_done,FinalizarSprintView
app_name = 'proyecto'

urlpatterns = [
    #URLS de proyecto
    path('', TemplateView.as_view(template_name="proyecto/index.html"),name='home'),
    path('proyectos/', ListaProyectos.as_view(), name='index'),
    path('proyecto/<int:pk>/', ProyectoDetailView.as_view(), name='detail'),
    path('proyecto/edit/<int:pk>/', edit, name='edit'),
    path('proyecto/create/', CreateProyectoView.as_view(), name='create'),
    path('proyecto/cancelar/<int:pk>/', cancelar, name='cancelar'),
    path('proyecto/proyectos-cancelados/', ListaProyectosCancelados.as_view(), name='cancelados'),
    path('proyecto/<int:pk_proy>/agregar-participantes/',AgregarParticipanteProyecto.as_view(), name='agregar-participantes-proyecto'),
    path('proyecto/<int:pk_proy>/debaja-participante/<int:pk>/',eliminarParticipanteView, name='debaja-participante-proyecto'),
    path('proyecto/<int:pk_proy>/agregar-desarrollador/',AgregarDesarrolladorView.as_view(), name='agregar-desarrollador-proyecto'),
    path('proyecto/<int:pk_proy>/editar-desarrollador/<int:dev_pk>/',EditDesarrolladorView.as_view(), name='editar-desarrollador-proyecto'),
    path('proyecto/<int:pk_proy>/sacar-desarrollador/<int:dev_pk>/',EliminarDesarrolladorView.as_view(), name='debaja-desarrollador-proyecto'),
    path('iniciar/proyecto/<int:pk>/', iniciar_proyecto, name='iniciar-proyecto'),
    path('cancelar/proyecto/<int:pk>/', cancelar_proyecto, name='cancelar-proyecto'),
    path('finalizar/proyecto/<int:pk>/', finalizar_proyecto, name='finalizar-proyecto'),

    #URLS de roles de proyecto
    path('proyecto/<int:pk_proy>/rol/agregar',agregar_rol_proyecto_view,name='agregar-rol'),
    path('proyecto/<int:pk_proy>/roles/',views.ListaRolProyectoView.as_view(),name = 'roles'),
    path('proyecto/<int:pk_proy>/roles/importar',ImportarRolView.as_view(),name = 'importar-roles'),
    path('proyecto/<int:pk_proy>/rol/<int:pk>', views.DetallesRolProyectoView.as_view(), name = 'rol-detalles'),
    path('proyecto/<int:pk_proy>/rol/<int:pk>/eliminar',views.EliminarRolProyectoView.as_view(),name = 'rol-eliminar'),
    path('proyecto/<int:pk_proy>/rol/<int:id_rol>/editar',editar_rol_proyecto_view,name='rol-editar'),
    path('proyecto/<int:pk_proy>/rol/<int:id_rol>/assignar',AssignUserRolProyecto.as_view(),name='rol-assignar'),

    path('proyecto/<int:pk_proy>/solicitud-permisos/',SolicitarPermisosView.as_view(),name='solicitud-permisos-proyecto'),

    path('proyecto/<int:pk_proy>/agregar-sprint/',AgregarSprintView.as_view(),name='agregar-sprint'),
    path('proyecto/<int:pk_proy>/sprint/<int:sprint_id>/',SprintView.as_view(),name='sprint-detail'),
    path('proyecto/<int:pk_proy>/sprint/<int:sprint_id>/edit/',SprintUpdateView.as_view(), name='sprint-edit'),
    path('proyecto/<int:pk_proy>/sprint/<int:pk>/team/',EquipoSprintUpdateView.as_view(),name='sprint-team-edit'),

    #URLS de user story
    path('proyecto/<int:pk_proy>/pbacklog',views.ProductBacklogView.as_view(),name='product-backlog'),
    path('proyecto/<int:pk_proy>/pbacklog/agregarUS',agregar_user_story_view,name='agregar-us'),
    path('proyecto/<int:pk_proy>/update-user-story/<int:us_id>',UserStoryUdateView.as_view(),name='user-story update'),
    path('proyecto/<int:pk_proy>/sprint/<int:sprint_id>/user-story/<int:us_id>/',UserStoryDetailView.as_view(),name='user-story-detail'),
    path('proyecto/<int:pk_proy>/sprint/<int:sprint_id>/user-story/<int:us_id>/quitar/',quitar_user_story_view,name='user-story-quitar'),
    path('proyecto/<int:pk_proy>/sprint/<int:sprint_id>/iniciar',iniciar_sprint_view,name='sprint-iniciar'),
    path('proyecto/<int:pk_proy>/sprint/<int:sprint_id>/finalizar',FinalizarSprintView.as_view(),name='sprint-finalizar'),
    path('proyecto/<int:pk_proy>/sprint/<int:sprint_id>/kanban/',SprintKanbanView.as_view(),name='sprint-kanban'),
    path('proyecto/<int:pk_proy>/user-story/<int:us_id>/',InspectUserStoryView.as_view(),name='user-story-detail-unassigned'),
    path('<int:pk_proy>/aprobar/user-story/<int:us_id>/', views.AprobarUserStoryView.as_view(), name='aprobar-user-story'),
    path('<int:pk_proy>/sprint/<int:sprint_id>/doing/user-story/<int:us_id>/', mark_us_doing, name='doing-user-story'),
    path('<int:pk_proy>/sprint/<int:sprint_id>/todo/user-story/<int:us_id>/', mark_us_todo, name='todo-user-story'),
    path('<int:pk_proy>/sprint/<int:sprint_id>/done/user-story/<int:us_id>/', mark_us_done, name='done-user-story'),
    path('proyecto/<int:pk_proy>/sprint/<int:sprint_id>/user-story-qa/<int:us_id>/',views.QaView.as_view(),name='user-story-qa'),

]
