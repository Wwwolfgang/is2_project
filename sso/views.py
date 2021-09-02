from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, DetailView,CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import User
from django.contrib.auth.models import Group
from .forms import UpdateRolSistemaForm, UserAssignRolForm

class ListaRolesSistema(ListView, LoginRequiredMixin):
    """ 
    Vista que genera el listado de los Roles de Sistema. Es llamada al entrar en la sección de 
    administración, que será accedida solo por los administradores de sistema. En el listado de roles se podrá modificar los roles.
    En esta pantalla también se verá el listado de todos los usuarios accedidos al sistema.
    Se podrá modificar y dar debaja a usuario y asignarles roles de sistema.
    """
    model = Group
    context_object_name = 'roles_sistema'
    template_name = 'sso/rolesSistema.html'
    raise_exception = True
    queryset = Group.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ListaRolesSistema, self).get_context_data(**kwargs)
        context.update({
            'usuarios': User.objects.exclude(first_name__isnull=True).exclude(first_name__exact=''),
        })
        return context

class UpdateRolSistema(UpdateView):
    """ Vista para actualizar los permisos de un rol de sistema """
    model = Group
    template_name = "sso/group_form.html"
    form_class = UpdateRolSistemaForm
    success_url = reverse_lazy('sso:roles-sistema-listado')


class DeleteUser(DeleteView):
    """ Vista para dar debaja de un Usuario """
    model = User
    success_url = reverse_lazy('sso:roles-sistema-listado')


class UpdateUser(UpdateView):
    """ Vista para actualizar el nombre, apellido y el estado de ser Administrador de un usuario. """
    model = User
    fields = [
        'is_administrator',
        'first_name',
        'last_name',
    ]
    success_url = reverse_lazy('sso:roles-sistema-listado')


class UserAssignSisRole(UpdateView):
    """
    Vista para asignarle roles de sistema al Usuario. Se conecta con el form
    UserAssignRolForm para gestionar el formulario.
    """
    model = User
    template_name = "sso/assignarRol.html"
    form_class = UserAssignRolForm
    raise_exception = True

    def get_object(self, queryset=None):
        id = self.kwargs['pk']
        return self.model.objects.get(id=id)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('sso:roles-sistema-listado'))
