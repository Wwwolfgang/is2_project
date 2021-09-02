from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, DetailView,CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import User
from django.contrib.auth.models import Group
from .forms import UpdateRolSistemaForm, UserAssignRolForm
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.base import ContextMixin
from .models import User
from django.contrib.auth.models import Group
from .forms import UpdateRolSistemaForm, UserAssignRolForm
from django.contrib import messages #import messages


class AdminUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Este mixin asegura, que solo administradores pueden acceder a las vistas donde se 
    aplicó el mixin. 
    """
    def test_func(self):
        """ En esta función, se hace un test si el usuario es administrador """
        return self.request.user.is_administrator

    def handle_no_permission(self):
        """ Si el usuario no es administrador, se muestra una alerta y se vuelve a la pagina de administración. """
        messages.error(self.request,'Usted no es Administrador!!')
        return HttpResponseRedirect(reverse('sso:roles-sistema-listado'))


class AdministrationUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Este mixin asegura, que solo administradores pueden acceder al listado de roles y de los usuarios.
    """
    def test_func(self):
        return self.request.user.is_administrator

    def handle_no_permission(self):
        messages.error(self.request,'Usted no es un Administrador!!')
        return HttpResponseRedirect(reverse('page-home'))

class ListaRolesSistema(AdministrationUserMixin,ListView):
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

    def get_context_data(self, **kwargs):
        context = super(ListaRolesSistema, self).get_context_data(**kwargs)
        context.update({
            'usuarios': User.objects.exclude(first_name__isnull=True).exclude(first_name__exact=''),
        })
        return context

class UpdateRolSistema(AdminUserMixin,UpdateView):
    """ Vista para actualizar los permisos de un rol de sistema """
    model = Group
    template_name = "sso/group_form.html"
    form_class = UpdateRolSistemaForm
    success_url = reverse_lazy('sso:roles-sistema-listado')


class DeleteUser(AdminUserMixin,DeleteView):
    """ Vista para dar debaja de un Usuario """
    model = User
    success_url = reverse_lazy('sso:roles-sistema-listado')


class UpdateUser(AdminUserMixin,UpdateView):
    """ Vista para actualizar el nombre, apellido y el estado de ser Administrador de un usuario. """
    model = User
    fields = [
        'is_administrator',
        'first_name',
        'last_name',
    ]
    success_url = reverse_lazy('sso:roles-sistema-listado')


class UserAssignSisRole(AdminUserMixin,UpdateView):
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
    
    def test_func(self):
        """ En esta función, se hace un test si el usuario quiere cambiar sus propios roles"""
        usuario = self.get_object()
        return self.request.user != usuario
    
    def handle_no_permission(self):
        """ Se devuelve un mensaje de error """
        messages.error(self.request,'Usted no es un Administrador o no puede cambiar sus propios roles')
        return HttpResponseRedirect(reverse('sso:roles-sistema-listado'))
