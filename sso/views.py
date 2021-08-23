from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, DetailView,CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.urls import reverse
from .models import RolSistema
from sso import models
from django.contrib import postgres
class ListaRolesSistema(ListView, LoginRequiredMixin):
    """ 
    Vista que genera el listado de los Roles de Sistema. Es llamada al entrar en la sección de 
    administración, que será accedida solo por los administradores de sistema.
    """

    context_object_name = 'RolesSistema'
    queryset = RolSistema.objects.all()
    template_name = 'rolesSistema.html'
    raise_exception = True
