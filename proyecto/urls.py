from . import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from proyecto.views import agregar_rol_proyecto_view
from django.urls import path
from django.views.generic import TemplateView
from .views import EliminarRolProyectoView, ProyectoDetailView, edit, delete, editar_rol_proyecto_view, ListaProyectos, AssignUserRolProyecto,ImportarRolView,iniciar_proyecto,cancelar_proyecto, CreateProyectoView
from .views import finalizar_proyecto, AgregarParticipanteProyecto, eliminarParticipanteView, AgregarDesarrolladorView,EditDesarrolladorView,EliminarDesarrolladorView,SolicitarPermisosView
app_name = 'proyecto'

urlpatterns = [
    #URLS de proyecto
    path('', TemplateView.as_view(template_name="proyecto/index.html"),name='home'),
    path('proyectos/', ListaProyectos.as_view(), name='index'),
    path('proyecto/<int:pk>/', ProyectoDetailView.as_view(), name='detail'),
    path('proyecto/edit/<int:pk>/', edit, name='edit'),
    path('proyecto/create/', CreateProyectoView.as_view(), name='create'),
    path('proyecto/delete/<int:pk>/', delete, name='delete'),
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
]
