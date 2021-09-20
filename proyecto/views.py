from django.db.models import Sum
import proyecto
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse
from proyecto import models
from proyecto.forms import AgregarRolProyectoForm, UserAssignRolForm, ImportarRolProyectoForm, ProyectoEditForm,ProyectoCreateForm,AgregarParticipanteForm, DesarrolladorCreateForm,PermisoSolicitudForm,SprintCrearForm, AgregarUserStoryForm
from proyecto.forms import EquipoFormset, UserStoryAssingForm, UserStoryDevForm
from proyecto.models import RolProyecto, Proyecto, ProyectUser, Sprint, UserStory, ProductBacklog
from django.views.generic.edit import UpdateView, DeleteView, FormView, CreateView
from django.urls import reverse_lazy
from guardian.decorators import permission_required_or_403,permission_required
from guardian.shortcuts import assign_perm
from sso.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from statistics import mean
from django.core.mail import send_mail

#Views de Rol Proyecto
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
            'proyecto_id': self.kwargs['pk_proy'],
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
            'proyecto': proyecto
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
        'proyecto_id': pk_proy
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
        'proyecto_id': pk_proy
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
            'proyecto_id': self.kwargs.get('pk_proy')
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
            'proyecto_id': self.kwargs['pk_proy'],
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

        form.save()
        for per in permisos:
            for participante in form.cleaned_data['participantes']:
                if per.content_type.model == 'proyecto':
                    user = participante
                    assign_perm(per,user,proyecto)
            for past_part in form.initial['participantes']:
                if per.content_type.model == 'proyecto':
                    if past_part not in form.cleaned_data['participantes']:
                        remove_perm(per,past_part,proyecto)


        else:   
            messages.error(self.request, 'Rol de proyecto no pudo ser assignado porque el proyecto no está activo')

        return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':self.kwargs['pk_proy']}))

#Views de proyecto
class ListaProyectos(PermissionRequiredMixin, ListView):
    permission_required = ('sso.pg_puede_acceder_proyecto','sso.pg_is_user')
    raise_exception = True
    model = Proyecto
    template_name = 'proyecto/index.html'
    context_object_name = 'proyecto_list'

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id).proyecto_set.all().exclude(estado_de_proyecto='C') | Proyecto.objects.filter(owner_id=self.request.user.id).exclude(estado_de_proyecto='C')


class ListaProyectosCancelados(PermissionRequiredMixin, ListView):
    permission_required = ('sso.pg_puede_acceder_proyecto','sso.pg_is_user')
    raise_exception = True
    model = Proyecto
    template_name = 'proyecto/proyectos-cancelados.html'
    context_object_name = 'proyecto_list_cancelados'

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id).proyecto_set.all().filter(estado_de_proyecto='C') | Proyecto.objects.filter(owner_id=self.request.user.id).filter(estado_de_proyecto='C')


class ProyectoDetailView(PermissionRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyecto/proyecto-detalle.html'
    permission_required = ('sso.pg_is_user','sso.pg_puede_acceder_proyecto')

    def get_object(self, queryset=None):
        id = self.kwargs['pk']

    def get_context_data(self, **kwargs):
        context = super(ProyectoDetailView,self).get_context_data(**kwargs)
        id = self.kwargs['pk']
        sprints = Sprint.objects.filter(proyecto__pk=id)
        proyecto = self.model.objects.get(id=id)
        self.request.session['proyecto_id'] = id
        self.request.session['proyecto_nombre'] = proyecto.nombreProyecto
        context.update({
            'proyecto': proyecto,
            'sprints': sprints
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
        ProductBacklog.objects.create(proyecto=get_object_or_404(Proyecto, pk=model.pkP))
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
def cancelar(request, pk, template_name='proyecto/confirm-cancel.html'):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method=='POST':
        proyecto.estado_de_proyecto = 'C'
        proyecto.save()
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


class AgregarDesarrolladorView(CreateView):
    model = ProyectUser
    template_name = "proyecto/proyecto_agregar_desarrollador.html"
    form_class = DesarrolladorCreateForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(AgregarDesarrolladorView,self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
        })
        return context

    def get_form_kwargs(self):
        """ Función que inyecta el id del proyecto como argumento. """
        kwargs = super(AgregarDesarrolladorView, self).get_form_kwargs()
        kwargs['pk_proy'] = self.kwargs['pk_proy']
        return kwargs

    def form_valid(self,form):
        proyecto = Proyecto.objects.get(id=self.kwargs['pk_proy'])
        dev = form.save()

        proyecto.equipo_desarrollador.add(dev)

        return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':self.kwargs['pk_proy']}))


class EditDesarrolladorView(PermissionRequiredMixin, UpdateView):
    """ Vista para agregar o invitar nuevos participantes al proyecto. Solo se muestran usuarios
    con el permiso mínimo, que todavía no fueron agregados y con no son el owner del proyecto.
    """
    model = ProyectUser
    permission_required = ('sso.pg_is_user')
    template_name = 'proyecto/proyecto_agregar_desarrollador.html'
    form_class= DesarrolladorCreateForm
    raise_exception = True

    def get_object(self, queryset=None):
        """ Función que retorna el proyecto cuyo equipo va ser modificado """
        id = self.kwargs['dev_pk']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super(EditDesarrolladorView,self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'edit': True
        })
        return context

    def get_form_kwargs(self):
        """ Función que inyecta el id del proyecto como argumento. """
        kwargs = super(EditDesarrolladorView, self).get_form_kwargs()
        kwargs['pk_proy'] = self.kwargs['pk_proy']
        return kwargs


    def form_valid(self, form):
        """
        En esta función se agrega los usuarios marcados por el usuario al campo equipo del proyecto
        """
        form.save()
        return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':self.kwargs['pk_proy']}))


class EliminarDesarrolladorView(PermissionRequiredMixin, DeleteView):
    """
    Vista para eliminar un rol de proyecto.
    Se selecciona un rol, se confirma la eliminación, y se retorna a la
    página que lista los roles.
    """
    model = ProyectUser
    template_name = 'proyecto/eliminar_desarrollador.html'
    permission_required = ('sso.pg_is_user')

    def get_object(self,queryset=None):
        id = self.kwargs['dev_pk']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super(EliminarDesarrolladorView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
        })
        return context

    def form_valid(self, form):
        """Valida los datos del form de eliminación de rol de sistema"""
        proyecto = Proyecto.objects.get(id=self.kwargs['pk_proy'])
        dev = form.save()
        proyecto.equipo_desarrollador.remove(dev)

        return HttpResponseRedirect(self.get_success_url(self.kwargs['pk_proy']))


    def get_success_url(self,**kwargs):
        return reverse_lazy('proyecto:roles',kwargs={'pk_proy':self.kwargs['pk_proy']})


class SolicitarPermisosView(FormView):
    template_name = "proyecto/solicitud_form.html"
    form_class = PermisoSolicitudForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(SolicitarPermisosView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
        })
        return context

    def form_valid(self,form):
        user = User.objects.get(pk=self.request.user.pk)
        proyecto = Proyecto.objects.get(id=self.kwargs['pk_proy'])
        send_mail(
            subject=form.cleaned_data['asunto'],
            message=form.cleaned_data['body'],
            from_email=user.email,
            recipient_list=[proyecto.owner.email]
        )
        return HttpResponseRedirect(reverse('proyecto:detail',kwargs={'pk':self.kwargs['pk_proy']}))


class AgregarSprintView(CreateView):
    model = Sprint
    template_name = "proyecto/agregar_sprint.html"
    form_class = SprintCrearForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(AgregarSprintView,self).get_context_data(**kwargs)
        sprints_count = Sprint.objects.filter(proyecto__id=self.kwargs['pk_proy']).exclude(estado_de_sprint='C').count()
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'count': sprints_count + 1,
            'sprint_count': Sprint.objects.filter(proyecto__id=self.kwargs['pk_proy']).filter(
            estado_de_sprint='I').count()

        })
        return context

    # def get_form_kwargs(self):
    #     """ Función que inyecta el id del proyecto como argumento. """
    #     kwargs = super(AgregarSprintView, self).get_form_kwargs()
    #     kwargs['pk_proy'] = self.kwargs['pk_proy']
    #     return kwargs

    def form_valid(self,form):
        proyecto = Proyecto.objects.get(pk = self.kwargs['pk_proy'])
        sprints_count = Sprint.objects.filter(proyecto__id=self.kwargs['pk_proy']).exclude(estado_de_sprint='C').count()
        obj = form.save(commit=True)
        obj.identificador = 'Sprint ' + str(sprints_count+1)
        obj.proyecto = proyecto
        obj.save()
        return HttpResponseRedirect(reverse('proyecto:detail',kwargs={'pk':self.kwargs['pk_proy']}))


class EquipoSprintUpdateView(SingleObjectMixin,FormView):

    model = Sprint
    template_name = 'proyecto/sprint_equipo_edit.html'

    def get_context_data(self, **kwargs):
        context = super(EquipoSprintUpdateView,self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'sprint': Sprint.objects.get(pk=self.kwargs['pk']),
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(Sprint.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(Sprint.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return EquipoFormset(**self.get_form_kwargs(),form_kwargs={'proyecto':self.kwargs['pk_proy']}, instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Equipo del sprint actualizado'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('proyecto:detail', kwargs={'pk': self.kwargs['pk_proy'],})

#Views de user story
@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
def agregar_user_story_view(request, pk_proy):
    """
    Vista para agregar un user story al product backlog.
    Se toman como parámetros el nombre, la descripción y el tiempo estimado por el scrum master.
    """
    contexto = {}
    contexto.update({
        'proyecto_id': pk_proy
    })
    if request.method == 'POST':      
        form = AgregarUserStoryForm(request.POST or None)
        #Si el form se cargó correctamente, lo guardamos
        if form.is_valid():
            backlog = ProductBacklog.objects.filter(proyecto__id=pk_proy).count()

            if backlog == 0:
                ProductBacklog.objects.create(proyecto=get_object_or_404(Proyecto, pk=pk_proy))
            
            backlog = ProductBacklog.objects.get(proyecto__pk=pk_proy)
            u_story = form.save()
            u_story.product_backlog = backlog
            u_story.creador = request.user
            u_story.save()
            #Redirigimos al product backlog
            return redirect('proyecto:product-backlog', pk_proy)  
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_user_story_view.html', context=contexto)
    else:
        form = AgregarUserStoryForm()
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_user_story_view.html', context=contexto)

class UserStoryUdateView(UpdateView):
    """ View para modificar user storys no aprobados. """
    model = UserStory
    form_class= AgregarUserStoryForm
    template_name = 'proyecto/nuevo_user_story_view.html'
    raise_exception = True

    def get_object(self, queryset=None):
        """ Función que retorna el user story que vamos a modificar. """
        id = self.kwargs['us_id']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        """ Función para inyectar variables de contexto que serán utilizados en el template."""
        context = super(UserStoryUdateView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'update': True,
        })
        return context

    def get_success_url(self):
        return reverse('proyecto:product-backlog', kwargs={'pk_proy': self.kwargs['pk_proy'],})


class ProductBacklogView(PermissionRequiredMixin, ListView):
    """ View de todos los user storys del proyecto. A la izquierda se ven los user storys temporales, a la derecha los aprobados que ya se encuentran el backlog. """
    model = UserStory
    template_name = 'proyecto/product_backlog.html'
    permission_required = ('sso.pg_is_user')

    def get_context_data(self, **kwargs):
        """ Función para inyectar variables de contexto que serán utilizados en el template."""
        context = super(ProductBacklogView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'user_storys_nuevos': ProductBacklog.objects.get(proyecto__pk = self.kwargs['pk_proy']).userstory_set.filter(estado_aprobacion='T'),
            'product_backlog': ProductBacklog.objects.get(proyecto__pk = self.kwargs['pk_proy']).userstory_set.filter(estado_aprobacion='A'),
        })
        return context


def aprobar_user_story(request,pk_proy,pk):
    """ View para aprobar un user story por un htmx post call. """
    if request.method == 'POST': 
        user_story = get_object_or_404(UserStory,pk=pk)
        user_story.estado_aprobacion = 'A'
        user_story.save()
    return HttpResponse('<a style="color: green;"  role="button"><i class="fas fa-check-square me-4"></i></i></a>')


class SprintView(TemplateView):
    """ View para ver el Sprint. Dependiendo del estado del sprint, el owner puede ver los user storys del backlog y los puede asignar.
        Los encargados y participantes del proyecto pueden ver los user storys asignados al sprint.
    """
    model = Sprint
    template_name = 'proyecto/sprint_detail.html'

    def get_context_data(self, **kwargs):
        """ Función para inyectar variables de contexto que serán utilizados en el template."""
        context = super(SprintView,self).get_context_data(**kwargs)
        sprint_backlog = UserStory.objects.filter(sprint__pk = self.kwargs['sprint_id'])
        total_us = sprint_backlog.count()
        ready_us = sprint_backlog.exclude(tiempo_promedio_calculado__isnull=True).count()
        if total_us == ready_us and total_us != 0:
            context.update({
                'ready_inicio': True
            })

        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'sprint': Sprint.objects.get(pk=self.kwargs['sprint_id']),
            'user_storys': ProductBacklog.objects.get(proyecto__pk = self.kwargs['pk_proy']).userstory_set.filter(estado_aprobacion='A').filter(sprint__isnull=True),
            'sprint_backlog': sprint_backlog,
            'owner': Proyecto.objects.get(pk=self.kwargs['pk_proy']).owner
        })
        return context


class UserStoryDetailView(UpdateView):
    """ 
    Vista para ver en detalle el user story. Es un updateview que será usado por el scrum master del proyecto y por el encargado asignado.
    Dependiendo de la persona que abre el link, se muestran los campos del form.

    """
    model = UserStory
    template_name = 'proyecto/userstory_detail_update.html'
    raise_exception = True

    def get_object(self, queryset=None):
        """ Función que retorna el user story"""
        id = self.kwargs['us_id']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        """ Función para inyectar variables de contexto que serán utilizados en el template."""
        context = super(UserStoryDetailView,self).get_context_data(**kwargs)
        sprint = get_object_or_404(Sprint,pk=self.kwargs['sprint_id'])
        if self.object.encargado != None:
            context.update({
                'is_assigned': True,
            })


        if sprint.estado_de_sprint == 'A':
            context.update({
                'sprint_activo': True,
            })
        else:
            context.update({
                'sprint_activo': False,
            })

        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'assignar': True,
            'scrum_master' : Proyecto.objects.get(pk=self.kwargs['pk_proy']).owner,
            'sprint_id': self.kwargs['sprint_id'],
        })
        return context

    def get_form_kwargs(self):
        """ Función que inyecta el id del sprint que se usa en el Form. """
        kwargs = super(UserStoryDetailView, self).get_form_kwargs()
        kwargs['sprint_id'] = self.kwargs['sprint_id']
        return kwargs

    def get_form_class(self):
        """ Función que devuelve el Form dependiendo si el usuario es el scrum master o no. """
        owner = Proyecto.objects.get(pk=self.kwargs['pk_proy']).owner
        if self.request.user == owner:
            return UserStoryAssingForm
        else:
            return UserStoryDevForm

    def form_valid(self, form):
        """ Función que hace calculos de promedio y envia un email al encargado, después de que se guardan los cambios del user story. """
        us = form.save()
        proyecto = get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])
        sprint = get_object_or_404(Sprint,pk=self.kwargs['sprint_id'])

        if us.tiempo_estimado_scrum_master != 0 and us.tiempo_estimado_scrum_master != None and us.tiempo_estimado_dev != 0 and us.tiempo_estimado_dev != None:
            us.tiempo_promedio_calculado = mean([us.tiempo_estimado_scrum_master,us.tiempo_estimado_dev])
            

        if self.request.user == proyecto.owner:
            us.sprint = sprint
            send_mail(
                subject='Se le asignó un nuevo user story',
                message='Se le acaba de asignar un nuevo user story, porfavor entre lo más posible en la plataforma para completar el tiempo estimado de terminación del user story.',
                from_email=proyecto.owner.email,
                recipient_list=[us.encargado.usuario.email],
            )
        us.save()
        sprint.carga_horaria = UserStory.objects.filter(sprint__id=self.kwargs['sprint_id']).aggregate(Sum('tiempo_promedio_calculado')).get('tiempo_promedio_calculado__sum',0.00)
        sprint.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'El user story fue asignado al sprint'
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """ Función que devuelve la dirección de salida. """
        return reverse('proyecto:sprint-detail', kwargs={'pk_proy': self.kwargs['pk_proy'],'sprint_id':self.kwargs['sprint_id']})


class InspectUserStoryView(DetailView):
    """  
    View para ver el user story en detalle. Esta vista será usada por personas que no sean el owner del proyecto.
    Se hizo esa división para manejar mejor los forms. Pero ambas vistas se van al mismo template.
    """
    model = UserStory
    template_name = 'proyecto/userstory_detail_update.html'
    raise_exception = True

    def get_object(self, queryset=None):
        """ Función que retorna el proyecto cuyo equipo va ser modificado """
        id = self.kwargs['us_id']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super(InspectUserStoryView,self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
        })
        return context


def quitar_user_story_view(request, pk_proy, sprint_id, us_id, template_name='proyecto/quitar_userstory_sprint.html'):
    """ 
    View para desasignar un user story del sprint. 
    Cuando el usuario realmente lo quiere desasignar, se quitan las horas estimadas, el sprint y el encargado previamentes asignados.
    """
    us = get_object_or_404(UserStory, pk=us_id)
    sprint = get_object_or_404(Sprint, pk=sprint_id)

    if request.method=='POST':
        us.sprint = None
        us.encargado = None
        us.tiempo_estimado_scrum_master = 0
        us.tiempo_estimado_dev = 0
        us.tiempo_promedio_calculado = 0
        sprint.carga_horaria = UserStory.objects.filter(sprint__id=sprint_id).aggregate(Sum('tiempo_promedio_calculado')).get('tiempo_promedio_calculado__sum',0.00)
        sprint.save()
        us.save()
        return HttpResponseRedirect(reverse('proyecto:sprint-detail',kwargs={'pk_proy':pk_proy,'sprint_id':sprint_id}))
    return render(request, template_name, {'proyecto_id':pk_proy, 'sprint_id':sprint_id, 'us_id': us_id})


def iniciar_sprint_view(request, pk_proy, sprint_id, template_name='proyecto/iniciar_sprint.html'):
    """ 
    View para iniciar un sprint. El botón solo será visible cuando todos los user storys asignados tienen tiempos estimados.
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)

    if request.method=='POST':
        sprint.estado_de_sprint = 'A'
        sprint.save()
        return HttpResponseRedirect(reverse('proyecto:sprint-detail',kwargs={'pk_proy':pk_proy,'sprint_id':sprint_id}))
    return render(request, template_name, {'proyecto_id':pk_proy, 'sprint_id':sprint_id})


class SprintKanbanView(TemplateView):
    """ 
    Vista del Tablero Kanban de un Sprint.
    Se muestran por el momento las tres columnas de Todo, Doing y Done.
    Por el momento todavia no se puede cambiar el estado de los user storys.
    TODO

    - cambiar estados de user storys
    - ver burndown chart
    """
    model = Sprint
    template_name = 'proyecto/sprint_kanban.html'

    def get_context_data(self, **kwargs):
        context = super(SprintKanbanView,self).get_context_data(**kwargs)
        sprint_backlog = UserStory.objects.filter(sprint__pk = self.kwargs['sprint_id'])
        us_todo = sprint_backlog.filter(estado_user_story='TD')
        us_doing = sprint_backlog.filter(estado_user_story='DG')
        us_done = sprint_backlog.filter(estado_user_story='DN')
        us_qa = sprint_backlog.filter(estado_user_story='QA')

        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'sprint': Sprint.objects.get(pk=self.kwargs['sprint_id']),
            'ready_inicio': True,
            'us_todo': us_todo,
            'us_doing':us_doing,
            'us_done':us_done,
            'us_qa':us_qa
        })
        return context