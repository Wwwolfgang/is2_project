from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from proyecto.views import EliminarRolProyecto, agregar_rol_proyecto_view, lista_rol_proyecto_view

urlpatterns = [
    path('addProjRol/',agregar_rol_proyecto_view),
    path('listaProjRol/',lista_rol_proyecto_view),
    #path('<int:pk>/delProjRol/',EliminarRolProyecto.as_view(), name='rolproyecto-eliminar')
]
