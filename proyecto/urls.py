from . import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from proyecto.views import agregar_rol_proyecto_view
from django.urls import path
from django.views.generic import TemplateView
from .views import EliminarRolProyectoView, ProyectoDetailView, edit, create, delete, IndexView, editar_rol_proyecto_view

app_name = 'proyecto'

urlpatterns = [
    #URLS de proyecto
    path('', TemplateView.as_view(template_name="proyecto/index.html"),name='home'),
    path('proyecto/', IndexView.as_view(), name='index'),
    path('proyecto/<int:pk>/', ProyectoDetailView.as_view(), name='detail'),
    path('proyecto/edit/<int:pk>/', edit, name='edit'),
    path('proyecto/create/', create, name='create'),
    path('proyecto/delete/<int:pk>/', delete, name='delete'),
    #URLS de roles de proyecto
    path('rol/agregar',agregar_rol_proyecto_view,name='agregar-rol'),
    path('proyecto/roles/',views.ListaRolProyectoView.as_view(),name = 'roles'),
    path('rol/<int:pk>', views.DetallesRolProyectoView.as_view(), name = 'rol-detalles'),
    path('proyecto/rol/<int:pk>/eliminar',views.EliminarRolProyectoView.as_view(),name = 'rol-eliminar'),
    path('proyecto/rol/<int:id_rol>/editar',editar_rol_proyecto_view,name='rol-editar'),

]
