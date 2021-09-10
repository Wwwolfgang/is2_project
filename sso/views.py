from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, DetailView,CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.base import ContextMixin
from .models import User
from django.contrib.auth.models import Group
from .forms import UpdateRolSistemaForm, UserAssignRolForm
from django.contrib import messages #import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
def enviar_solicitud_accesso_view(request, pk):
    user = User.objects.get(pk=pk)
    send_mail(
        subject='Usuario nuevo - solicitud de Accesso',
        message='Hola mi nombre es ' + user.first_name + ' ' + user.last_name
        + '\n' + 'Inicié sesión en la aplicación Gestión de Proyectos. Envio esta solicitud porque no tengo permisos y no puedo hacer nada.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.RECIPIENT_ADDRESS]
    )
    return HttpResponse("Solicitud enviada")
class AdminUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Este mixin asegura, que solo administradores pueden acceder a las vistas donde se 
    aplicó el mixin. 
    En caso de error envia un mensaje que será visible en la página.
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
    En caso de error envia un mensaje que será visible en la página.
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

class UpdateRolSistema(AdminUserMixin,UpdateView):
    """ Vista para actualizar los permisos de un rol de sistema. Retorna un 
    listado de permisos de los cuales se puede asignar nuevos permisos o quitar permisos del rol.
    """
    model = Group
    template_name = "sso/group_form.html"
    form_class = UpdateRolSistemaForm
    success_url = reverse_lazy('sso:roles-sistema-listado')


class DeleteUser(AdminUserMixin,DeleteView):
    """ Vista para dar debaja del sistema de un Usuario """
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
        """ Función que retorna el usuario al cual se va asignar los roles. """
        id = self.kwargs['pk']
        return self.model.objects.get(id=id)

    def form_valid(self, form):
        """ Función para validar el Form. Guarda el form y redirecciona a la pagina de administración. """
        form.save()
        return HttpResponseRedirect(reverse('sso:roles-sistema-listado'))
    
    # def test_func(self):
    #     """ En esta función, se hace un test si el usuario quiere cambiar sus propios roles"""
    #     usuario = self.get_object()
    #     return self.request.user != usuario
    
    # def handle_no_permission(self):
    #     """ Se devuelve un mensaje de error """
    #     messages.error(self.request,'Usted no es un Administrador o no puede cambiar sus propios roles')
    #     return HttpResponseRedirect(reverse('sso:roles-sistema-listado'))