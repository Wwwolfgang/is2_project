from django.contrib import messages
from django.contrib.auth import models
from django.contrib.auth.models import Permission
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse
from proyecto.forms import AgregarRolProyectoForm, UserAssignRolForm, ImportarRolProyectoForm, ProyectoEditForm,ProyectoCreateForm,AgregarParticipanteForm
from proyecto.models import RolProyecto, Proyecto
from django.views.generic.edit import UpdateView, DeleteView, FormView, CreateView
from django.urls import reverse_lazy
from guardian.decorators import permission_required_or_403,permission_required
from guardian.shortcuts import assign_perm
from sso.models import User
from django.views.decorators.csrf import csrf_exempt
import json

class EliminarRolProyectoView(PermissionRequiredMixin, DeleteView):
    """
    Vista para eliminar un rol de proyecto.
    Se selecciona un rol, se confirma la eliminación, y se retorna a la
    página que lista los roles.
    """
    model = RolProyecto
    template_name = 'proyecto/eliminar_rol_proyecto.html'
    permission_required = ('sso.pg_is_user')

    def get_context_data(self, **kwargs):
        context = super(EliminarRolProyectoView, self).get_context_data(**kwargs)
        context.update({
            'proyect_id': self.kwargs['pk_proy'],
        })
        return context

    def form_valid(self, form):
        """Valida los datos del form de eliminación de rol de sistema"""
        form.save()
        return HttpResponseRedirect(self.get_success_url(self.kwargs['pk_proy']))


    def get_success_url(self,**kwargs):
        return reverse_lazy('proyecto:roles',kwargs={'pk_proy':self.kwargs['pk_proy']})
    

class ListaRolProyectoView(PermissionRequiredMixin, ListView):
    """
    Vista para listar los roles asociados a un proyecto.
    Se presiona el botón de "Roles" y se despliega la lista de roles.
    """
    model = RolProyecto
    template_name = 'proyecto/lista_rol_proyecto.html'
    permission_required = ('sso.pg_is_user')

    def get_context_data(self, **kwargs):
        context = super(ListaRolProyectoView,self).get_context_data(**kwargs)
        proyecto = get_object_or_404(Proyecto, pk=self.kwargs.get('pk_proy'))
        user = User.objects.filter(pk=proyecto.owner.pk)
        context.update({
            'roles': RolProyecto.objects.filter(proyecto__id= self.kwargs.get('pk_proy')),
            'participantes': proyecto.equipo.all() | user,
            'proyect': proyecto
        })
        return context


class DetallesRolProyectoView(PermissionRequiredMixin, DetailView):
    model = RolProyecto
    permission_required = ('sso.pg_is_user')
    template_name = 'proyecto/detalles_rol_proyecto.html'


@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
def agregar_rol_proyecto_view(request,pk_proy):
    """
    Vista para agregar un rol de proyecto al proyecto.
    Se toman como parámetros el nombre del nuevo rol y sus permisos asociados para crear el rol.
    """
    contexto = {}
    contexto.update({
        'proyect_id': pk_proy
    })
    if request.method == 'POST':
        form = AgregarRolProyectoForm(request.POST or None)
        #Si el form se cargó correctamente, lo guardamos
        if form.is_valid():
            obj = form.save(commit=True)
            proyecto = get_object_or_404(Proyecto, pk=pk_proy)
            obj.proyecto = proyecto
            obj.save()
            return redirect('proyecto:roles', pk_proy)  
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_rol_proyecto_view.html', context=contexto)
    else:
        form = AgregarRolProyectoForm()   
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_rol_proyecto_view.html', context=contexto)


@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
def editar_rol_proyecto_view(request, pk_proy, id_rol):
    """
    Vista para editar el rol de un proyecto.
    Al seleccionar el rol a editar se despliegan las opciones para renombrar el rol y reasignar los
    permisos.
    """
    rol = get_object_or_404(RolProyecto, pk=id_rol)
    contexto = {}

    contexto.update({
        'proyect_id': pk_proy
    })
    if request.method == 'POST':
        form = AgregarRolProyectoForm(request.POST, instance=rol)

        if form.is_valid(): 
            rol = form.save()
            messages.success(request, 'Rol de proyecto actualizado exitosamente')
            return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':pk_proy}))
        contexto['form'] = form
        return render(request, 'proyecto/editar_rol_proyecto.html', context=contexto)
    else:
        form = AgregarRolProyectoForm(instance=rol, initial={'permisos': [r.id for r in rol.get_permisos()]})   
        contexto['form'] = form
        return render(request, 'proyecto/editar_rol_proyecto.html', contexto)


class ImportarRolView(PermissionRequiredMixin, FormView):
    """ Vista para la importación de roles de otros proyectos. Da la lista de todos los roles que no están
    asociados al proyecto, de los cuales se puede importar los roles al proyecto. """
    template_name = 'proyecto/importar_rol.html'
    permission_required = ('sso.pg_is_user')
    form_class= ImportarRolProyectoForm

    def get_context_data(self, **kwargs):
        """ Inyecta los roles y el proyect_id al contexto. """
        context = super(ImportarRolView,self).get_context_data(**kwargs)
        context.update({
            'roles': RolProyecto.objects.exclude(proyecto__id= self.kwargs.get('pk_proy')),
            'proyect_id': self.kwargs.get('pk_proy')
        })
        return context

    def form_valid(self, form):
        """Valida los datos del form de eliminación de rol de sistema"""
        proyecto = Proyecto.objects.get(id=self.kwargs['pk_proy'])
        for rol in form.cleaned_data['roles']:
            rol = RolProyecto.objects.get(id=rol)
            permisos = RolProyecto.objects.get(id=rol.id).permisos.all().values_list('pk', flat=True)
            rol.pk = None
            rol.proyecto = proyecto
            rol.save()
            for permiso in permisos:
                rol.permisos.add(permiso)
            rol.save()

        return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':self.kwargs['pk_proy']}))

    def get_form_kwargs(self):
        """ Función que inyecta el id del proyecto como argumento. """
        kwargs = super(ImportarRolView, self).get_form_kwargs()
        kwargs['pk_proy'] = self.kwargs['pk_proy']
        return kwargs


class AssignUserRolProyecto(PermissionRequiredMixin, UpdateView):
    """ Vista para assignarle a los usuarios el rol de proyecto """
    model = RolProyecto
    permission_required = ('sso.pg_is_user')
    template_name = 'proyecto/user_assign_rol.html'
    form_class= UserAssignRolForm
    raise_exception = True

    def get_object(self, queryset=None):
        """ Función que retorna el rol que vamos asignar a los usuarios. """
        id = self.kwargs['id_rol']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super(AssignUserRolProyecto, self).get_context_data(**kwargs)
        context.update({
            'proyect_id': self.kwargs['pk_proy'],
        })
        return context

    def get_form_kwargs(self):
        """ Función que inyecta el id del proyecto como argumento. """
        kwargs = super(AssignUserRolProyecto, self).get_form_kwargs()
        kwargs['pk_proy'] = self.kwargs['pk_proy']
        return kwargs

    def form_valid(self, form):
        """
        Valida los datos del form de la asignación del rol.
        primero obtiene el proyecto y el rol. Si el form es válido, assigna a cada participante seleccionado los permisos del rol por el objeto actual.
        En caso de que el proyecto no está activo, no se puede assignar el rol.
        """
        proyecto = Proyecto.objects.get(id=self.kwargs['pk_proy'])
        permisos = RolProyecto.objects.get(id=self.kwargs['id_rol']).permisos.all()

        if proyecto.estado_de_proyecto == 'A':
            form.save()
            for per in permisos:
                for participante in form.cleaned_data['participantes']:
                    if per.content_type.model == 'proyecto':
                        user = User.objects.get(id=participante)
                        assign_perm(per,user,proyecto)

        else:   
            messages.error(self.request, 'Rol de proyecto no pudo ser assignado porque el proyecto no está activo')

        return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':self.kwargs['pk_proy']}))


class ListaProyectos(PermissionRequiredMixin, ListView):
    permission_required = ('sso.pg_puede_acceder_proyecto','sso.pg_is_user')
    raise_exception = True
    model = Proyecto
    template_name = 'proyecto/index.html'
    context_object_name = 'proyecto_list'

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id).proyecto_set.all().exclude(estado_de_proyecto='C') | Proyecto.objects.filter(owner_id=self.request.user.id).exclude(estado_de_proyecto='C')


class ProyectoDetailView(PermissionRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyecto/proyecto-detalle.html'
    permission_required = ('sso.pg_is_user','sso.pg_puede_acceder_proyecto')

    def get_object(self, queryset=None):
        id = self.kwargs['pk']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super(ProyectoDetailView,self).get_context_data(**kwargs)
        id = self.kwargs['pk']
        proyecto = self.model.objects.get(id=id)
        self.request.session['proyect_id'] = id
        self.request.session['proyect_name'] = proyecto.nombreProyecto
        context.update({
            'proyect': json.dumps(
                {
                    'id': proyecto.id,
                    'nombre': proyecto.nombreProyecto,
                    'estado': proyecto.estado_de_proyecto,
                    'duracionSprint': proyecto.duracionSprint
                }
            )
        }) 
        return context


class CreateProyectoView(CreateView):
    model = Proyecto
    template_name = "proyecto/proyecto_form.html"
    form_class = ProyectoCreateForm
    raise_exception = True

    def get_form_kwargs(self):
        """ Función que inyecta el id del proyecto como argumento. """
        kwargs = super(CreateProyectoView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def form_valid(self,form):
        user = User.objects.get(pk =self.request.user.id)
        model = form.save()
        model.save()
        model.owner = user
        model.save()
        return HttpResponseRedirect(reverse('proyecto:index'))


class AgregarParticipanteProyecto(PermissionRequiredMixin, UpdateView):
    """ Vista para agregar o invitar nuevos participantes al proyecto. Solo se muestran usuarios
    con el permiso mínimo, que todavía no fueron agregados y con no son el owner del proyecto.
    """
    model = Proyecto
    permission_required = ('sso.pg_is_user')
    template_name = 'proyecto/agregar_participantes.html'
    form_class= AgregarParticipanteForm
    raise_exception = True

    def get_object(self, queryset=None):
        """ Función que retorna el proyecto cuyo equipo va ser modificado """
        id = self.kwargs['pk_proy']
        return self.model.objects.get(id=id)


    def form_valid(self, form):
        """
        En esta función se agrega los usuarios marcados por el usuario al campo equipo del proyecto
        """
        proyecto = Proyecto.objects.get(id=self.kwargs['pk_proy'])
        equipo = form.cleaned_data['equipo']
        for usuario in equipo:
            user = User.objects.get(pk=usuario)
            proyecto.equipo.add(user)
        return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':self.kwargs['pk_proy']}))


def eliminarParticipanteView(request, pk_proy, pk, template_name='proyecto/delete_confirm_participante.html'):
    """ View para eliminar participantes de equipo de un proyecto. Es una vista de confirmación
        , si el usuario elige "Eliminar" se elimina el usuario del proyecto.
    """
    proyecto = get_object_or_404(Proyecto, pk=pk_proy)
    user = get_object_or_404(User, pk=pk)

    if request.method=='POST':
        proyecto.equipo.remove(user)
        return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':pk_proy}))
    return render(request, template_name, {'object':proyecto, 'usuario':user})


@permission_required('sso.pg_puede_acceder_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_puede_crear_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
def edit(request, pk, template_name='proyecto/edit.html'):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    form = ProyectoEditForm(request.POST or None, instance=proyecto)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('proyecto:index'))
    return render(request, template_name, {'form':form})


@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
def delete(request, pk, template_name='proyecto/confirm-delete.html'):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method=='POST':
        proyecto.delete()
        return HttpResponseRedirect(reverse('proyecto:index'))
    return render(request, template_name, {'object':proyecto})

@csrf_exempt
@permission_required('sso.pg_puede_acceder_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_puede_crear_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
def iniciar_proyecto(request, pk):
    proyecto = Proyecto.objects.get(pk=pk)
    proyecto.estado_de_proyecto = 'A'
    proyecto.save()
    return HttpResponse("Iniciado")

@csrf_exempt
@permission_required('sso.pg_puede_acceder_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_puede_crear_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
def cancelar_proyecto(request, pk):
    proyecto = Proyecto.objects.get(pk=pk)
    proyecto.estado_de_proyecto = 'C'
    proyecto.save()
    return HttpResponse("Cancelado")

@csrf_exempt
@permission_required('sso.pg_puede_acceder_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_puede_crear_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
def finalizar_proyecto(request, pk):
    proyecto = Proyecto.objects.get(pk=pk)
    proyecto.estado_de_proyecto = 'F'
    proyecto.save()
    return HttpResponse("Finalizado")