from . import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from proyecto.views import agregar_rol_proyecto_view,lista_rol_proyecto_view
from django.urls import path
from django.views.generic import TemplateView
from .views import ProyectoDetailView, edit, create, delete, ListaProyectos

app_name = 'proyecto'

urlpatterns = [
    path('', TemplateView.as_view(template_name="proyecto/index.html"),name='home'),
    path('proyecto/', ListaProyectos.as_view(), name='index'),
    path('proyecto/<int:pk>/', ProyectoDetailView.as_view(), name='detail'),
    path('proyecto/edit/<int:pk>/', edit, name='edit'),
    path('proyecto/create/', create, name='create'),
    path('proyecto/delete/<int:pk>/', delete, name='delete'),
    path('rol/agregar',agregar_rol_proyecto_view),
    path('rol/listar',lista_rol_proyecto_view),
    path('roles/',views.ListaRolProyectoView.as_view(),name = 'roles'),
    path('rol/<int:pk>', views.DetallesRolProyectoView.as_view(), name = 'rol-detalles')
]
