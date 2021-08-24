from . import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from proyecto.views import agregar_rol_proyecto_view,lista_rol_proyecto_view

urlpatterns = [
    path('rol/agregar',agregar_rol_proyecto_view),
    path('rol/listar',lista_rol_proyecto_view),
    path('roles/',views.ListaRolProyectoView.as_view(),name = 'roles'),
    path('rol/<int:pk>', views.DetallesRolProyectoView.as_view(), name = 'rol-detalles')
]
