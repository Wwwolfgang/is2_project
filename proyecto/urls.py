from .views import ListaParticipantes, UserStoryView
from . import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from proyecto.views import agregar_rol_proyecto_view
from django.urls import path
from django.views.generic import TemplateView
from .views import EliminarRolProyectoView, ProyectoDetailView, edit, create, delete, editar_rol_proyecto_view, ListaProyectos, AssignUserRolProyecto,ImportarRolView

app_name = 'proyecto'

urlpatterns = [
    #URLS de proyecto
    path('', TemplateView.as_view(template_name="proyecto/index.html"),name='home'),
    path('proyectos/', ListaProyectos.as_view(), name='index'),
    path('proyecto/<int:pk>/', ProyectoDetailView.as_view(), name='detail'),
    path('proyecto/edit/<int:pk>/', edit, name='edit'),
    path('proyecto/create/', create, name='create'),
    path('proyecto/delete/<int:pk>/', delete, name='delete'),
    #URLS de roles de proyecto
    path('proyecto/<int:pk_proy>/rol/agregar',agregar_rol_proyecto_view,name='agregar-rol'),
    path('proyecto/<int:pk_proy>/roles/',views.ListaRolProyectoView.as_view(),name = 'roles'),
    path('proyecto/<int:pk_proy>/roles/importar',ImportarRolView.as_view(),name = 'importar-roles'),
    path('proyecto/<int:pk_proy>/rol/<int:pk>', views.DetallesRolProyectoView.as_view(), name = 'rol-detalles'),
    path('proyecto/<int:pk_proy>/rol/<int:pk>/eliminar',views.EliminarRolProyectoView.as_view(),name = 'rol-eliminar'),
    path('proyecto/<int:pk_proy>/rol/<int:id_rol>/editar',editar_rol_proyecto_view,name='rol-editar'),
    path('proyecto/<int:pk_proy>/rol/<int:id_rol>/assignar',AssignUserRolProyecto.as_view(),name='rol-assignar'),
    path('', TemplateView.as_view(template_name="proyecto/index.html")),
    path('proyecto/participante/agregar',ListaParticipantes.as_view(), name = 'participantes'),
    #URLS de user story
    path('proyecto/userstory/',UserStoryView.as_view(),name='user-story'),
    #path('proyecto/userstory/agregar',UserStoryView.agregar(),name='user-story-agregar'),
    #path('proyecto/userstory/listar',UserStoryView.listar(),name='user-story-listar'),
    #path('proyecto/userstory/modificar',UserStoryView.modificar(),name='user-story-modificar'),
    #path('proyecto/userstory/cancelar',UserStoryView.cancelar(),name='user-story-cancelar'),
]
