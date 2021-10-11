from django.contrib.auth.models import Permission
from django.db.models import Sum
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm, remove_perm, get_user_perms
from django.forms.models import model_to_dict
#Mixin de django por defecto
#from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
#Usamos el mixin de Django Guardian
from guardian.mixins import PermissionRequiredMixin 
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse
import proyecto
from proyecto.forms import AgregarRolProyectoForm, UserAssignRolForm, ImportarRolProyectoForm, ProyectoEditForm,ProyectoCreateForm,AgregarParticipanteForm, DesarrolladorCreateForm,PermisoSolicitudForm,SprintCrearForm, AgregarUserStoryForm
from proyecto.forms import EquipoFormset, UserStoryAssingForm, UserStoryDevForm, SprintModificarForm, SprintFinalizarForm, QaForm, UserstoryAprobarForm, ProyectoFinalizarForm, DailyForm
from proyecto.models import RolProyecto, Proyecto, ProyectUser, Sprint, UserStory, ProductBacklog, HistorialUS, Daily
from django.views.generic.edit import UpdateView, DeleteView, FormView, CreateView
from django.urls import reverse_lazy
from guardian.decorators import permission_required_or_403,permission_required
from guardian.shortcuts import assign_perm
from sso.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from statistics import mean
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.core.serializers import serialize
from decimal import Decimal


class EliminarRolProyectoView(DeleteView):
    """
    Vista para eliminar un rol de proyecto.
    Se selecciona un rol, se confirma la eliminación, y se retorna a la
    página que lista los roles.
    """
    model = RolProyecto
    template_name = 'proyecto/eliminar_rol_proyecto.html'
    # permission_required = ('proyecto.p_administrar_roles')
    raise_exception = True

    def get_object(self, queryset=None):
        """ Función que retorna el rol que vamos asignar a los usuarios. """
        id = self.kwargs['pk']
        return self.model.objects.get(id=id)

    def dispatch(self, request, *args, **kwargs):
        """ Función que controla que no hayan participantes asignados al rol que se desea eliminar. Si hay participantes no se puede
        eliminar el rol y se vuelve a la ruta anterior
        """
        rol = get_object_or_404(RolProyecto,pk=kwargs['pk'])
        next = request.GET.get('next')
        if rol.participantes.all().count() != 0:
            messages.warning(request, '¡Hay usuarios que fueron asignados a este rol, no se puede eliminar el rol si tiene usuarios asignados!')
            return HttpResponseRedirect(next)
        return super().dispatch(request, *args, **kwargs)

    def get_permission_object(self):
        """ Función que devuelve el proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

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
    

class ListaRolProyectoView(ListView):
    """
    Vista para listar los roles y participantes asociados a un proyecto.
    Se presiona el botón de "Roles" y se despliega la lista de roles y participantes. Desde esta pantalla se puede agregar, importar, modificar, eliminar y
    asignar roles de proyecto. Además es posible agregar nuevos participantes o quitar participantes.
    """
    model = RolProyecto
    template_name = 'proyecto/lista_rol_proyecto.html'

    def get_permission_object(self):
        """ Función que devuelve el proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

    def get_context_data(self, **kwargs):
        """ Función que inyecta todas las variables de contexto al template """
        context = super(ListaRolProyectoView,self).get_context_data(**kwargs)
        proyecto = get_object_or_404(Proyecto, pk=self.kwargs.get('pk_proy'))
        user = User.objects.filter(pk=proyecto.owner.pk)
        context.update({
            'roles': RolProyecto.objects.filter(proyecto__id= self.kwargs.get('pk_proy')),
            'participantes': proyecto.equipo.all() | user,
            'proyecto': proyecto
        })
        return context


@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
@permission_required_or_403('proyecto.p_administrar_roles',(Proyecto,'pk','pk_proy'))
def agregar_rol_proyecto_view(request, pk_proy):
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
@permission_required_or_403('proyecto.p_administrar_roles',(Proyecto,'pk','pk_proy'))
def editar_rol_proyecto_view(request, pk_proy, id_rol):
    """
    Vista para editar el rol de un proyecto.
    Al seleccionar el rol a editar se despliegan las opciones para renombrar el rol y reasignar los
    permisos.
    En este rol si se modifica el rol se actualizan los permisos, es decir se asigna los nuevos permisos a los usuarios del rol y se quita los permisos 
    quitados de los usuarios.
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
            proyecto = Proyecto.objects.get(id=pk_proy)
            for per in rol.permisos.all():
                for participante in rol.participantes.all():
                    if per.content_type.model == 'proyecto':
                        user = participante
                        assign_perm(per,user,proyecto)
            for past_part in form.initial['permisos']:
                for participante in rol.participantes.all():
                    if past_part not in form.cleaned_data['permisos']:
                        if per.content_type.model == 'proyecto':
                            remove_perm(per,participante,proyecto)
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
    permission_required = ('proyecto.p_administrar_roles')
    form_class= ImportarRolProyectoForm
    raise_exception = True

    def get_object(self):
        """ Retorna el Proyecto al cual se importa el nuevo rol"""
        self.obj = get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])
        return self.obj

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


class AssignUserRolProyecto(PermissionRequiredMixin,UpdateView):
    """ Vista para assignarle a los usuarios el rol de proyecto. Si es asignado a un nuevo usuario se le asignan todos los permisos del rol. Si un usuario fue 
    desasignado, se le quitan todos los permisos del rol
    """
    model = RolProyecto
    #permission_required = ('proyecto.p_administrar_roles')
    permission_required = ('proyecto.p_administrar_roles')
    template_name = 'proyecto/user_assign_rol.html'
    form_class= UserAssignRolForm
    raise_exception = True

    def get_object(self, queryset=None):
        """ Función que retorna el rol que vamos asignar a los usuarios. """
        id = self.kwargs['id_rol']
        return self.model.objects.get(id=id)

    def get_permission_object(self):
        """ Función que devuelve el proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

    def get_context_data(self, **kwargs):
        """ Función que inyecta todas las variables de contexto que se utilizan en el template """
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


        # else:   
        #     messages.error(self.request, 'Rol de proyecto no pudo ser assignado porque el proyecto no está activo')

        return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':self.kwargs['pk_proy']}))
#Views de proyecto

class ListaProyectos(PermissionRequiredMixin, ListView):
    """ Listado de todos los proyectos a los cuales el usuario tiene acceso. Puede hacer algunas acciones como editar, eliminar, etc. o entrar en el proyecto. """
    permission_required = ('sso.pg_puede_acceder_proyecto','sso.pg_is_user')
    raise_exception = True
    model = Proyecto
    template_name = 'proyecto/index.html'
    context_object_name = 'proyecto_list'

    def get_queryset(self):
        proyectos = User.objects.get(id=self.request.user.id).proyecto_set.exclude(estado_de_proyecto='C') | Proyecto.objects.filter(owner_id=self.request.user.id).exclude(estado_de_proyecto='C')
        return proyectos.distinct()


class ListaProyectosCancelados(PermissionRequiredMixin, ListView):
    """ Vista que muestra todos los proyectos que fueron cancelados. Ya que los proyectos no se eliminan sino son cancelados aqui se ve solo proyectos cancelados. """
    permission_required = ('sso.pg_puede_acceder_proyecto','sso.pg_is_user')
    raise_exception = True
    model = Proyecto
    template_name = 'proyecto/proyectos-cancelados.html'
    context_object_name = 'proyecto_list_cancelados'

    def get_queryset(self):
        """ Función que devuelve los proyectos cancelados asociados al usuario """
        return User.objects.get(id=self.request.user.id).proyecto_set.all().filter(estado_de_proyecto='C') | Proyecto.objects.filter(owner_id=self.request.user.id).filter(estado_de_proyecto='C')


class ProyectoDetailView(PermissionRequiredMixin, DetailView):
    """ Vista global del proyecto, se ven los sprints, los user storys,etc. También se inicializa un barra global del proyecto para poder acceder rapidamente
        a controles del proyecto.
    """
    model = Proyecto
    template_name = 'proyecto/proyecto-detalle.html'
    permission_required = ('sso.pg_is_user','sso.pg_puede_acceder_proyecto')

    def get_object(self, queryset=None):
        """ Función que devuelve el proyecto """
        id = self.kwargs['pk']

    def get_context_data(self, **kwargs):
        """ Función que inyecta las variables de contexto al template, en este caso el proyecto y el listado de sus sprints """
        context = super(ProyectoDetailView,self).get_context_data(**kwargs)
        id = self.kwargs['pk']
        Sprints = Sprint.objects.filter(proyecto__pk=id)
        proyecto = self.model.objects.get(id=id)
        self.request.session['proyecto_id'] = id
        self.request.session['proyecto_nombre'] = proyecto.nombreProyecto
        context.update({
            'proyecto': proyecto,
            'sprints': Sprints
        }) 
        return context


class CreateProyectoView(PermissionRequiredMixin,CreateView):
    """ Vista para crear proyectos. En esta vista por el momento solo se llenan la duracion del sprint y la fecha de finalización. 
        Hay que evaluar que más campos se van a tratar aqui.
    """
    model = Proyecto
    template_name = "proyecto/proyecto_form.html"
    form_class = ProyectoCreateForm
    raise_exception = True
    permission_required = ('sso.pg_puede_crear_proyecto')

    def form_valid(self,form):
        """ Función que guarda el nuevo proyecto, le agrega el owner, crea un nuevo product backlog y asigna todos los permisos posibles al 
        owner del proyecto
        """
        user = User.objects.get(pk =self.request.user.id)
        model = form.save()
        model.save()
        model.owner = user
        model.estado_de_proyecto = 'A'
        model.save()
        ProductBacklog.objects.create(proyecto=get_object_or_404(Proyecto, pk=model.pk))
        #Aquí asignamos todos los permisos para el proyecto al creador del proyecto
        proyecto=get_object_or_404(Proyecto, pk=model.pk)
        for p in Permission.objects.all():
            if (p.codename.startswith('p_') and not p.codename.startswith('pg_')):
                    if p.content_type.model == 'proyecto':
                        assign_perm(p,user,proyecto)
        return HttpResponseRedirect(reverse('proyecto:index'))

    def get_form_kwargs(self):
        """ Función que inyecta el usuario al form como argumento. """
        kwargs = super(CreateProyectoView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs
    
    def get_object(self): 
        return None


class AgregarParticipanteProyecto(PermissionRequiredMixin, UpdateView):
    """ Vista para agregar o invitar nuevos participantes al proyecto. Solo se muestran usuarios
    con el permiso mínimo, que todavía no fueron agregados y con no son el owner del proyecto.
    """
    model = Proyecto
    permission_required = ('proyecto.p_administrar_participantes')
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


@permission_required_or_403('proyecto.p_administrar_participantes',(Proyecto,'pk','pk_proy'))
def eliminarParticipanteView(request, pk_proy, pk, template_name='proyecto/delete_confirm_participante.html'):
    """ View para eliminar participantes de equipo de un proyecto. Es una vista de confirmación
        , si el usuario elige "Eliminar" se elimina el usuario del proyecto.
    """
    proyecto = get_object_or_404(Proyecto, pk=pk_proy)
    user = get_object_or_404(User, pk=pk)
    roles = proyecto.rolproyecto_set.all()

    if request.method=='POST':
        for rol in roles:
            if rol.participantes.filter(pk=user.pk).exists():
                rol.participantes.remove(user)

        permisos = get_user_perms(user,proyecto)
        for per in permisos:
            remove_perm(per,user,proyecto)
        proyecto.equipo.remove(user)
        return HttpResponseRedirect(reverse('proyecto:roles',kwargs={'pk_proy':pk_proy}))
    return render(request, template_name, {'object':proyecto, 'usuario':user})


@permission_required('sso.pg_puede_acceder_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_puede_crear_proyecto', return_403=True, accept_global_perms=True)
@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
@permission_required_or_403('proyecto.p_editar_proyectos',(Proyecto,'pk','pk'))
def edit(request, pk, template_name='proyecto/edit.html'):
    """ Vista para editar algunos atributos del proyecto como la duracion del sprint y la fecha de finalizacion. """
    proyecto = get_object_or_404(Proyecto, pk=pk)
    form = ProyectoEditForm(request.POST or None, instance=proyecto)
    contexto = {}
    contexto.update({
        'proyecto_id': pk,
        'form':form
    })
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('proyecto:index'))
    return render(request, template_name, context=contexto)


@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
@permission_required_or_403('proyecto.p_cancelar_proyectos',(Proyecto,'pk','pk'))
def cancelar(request, pk, template_name='proyecto/confirm-cancel.html'):
    """ View para cancelar un proyecto. TODO se debería hacer cierto control cuando se puede cancelar un proyecto"""
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method=='POST':
        proyecto.estado_de_proyecto = 'C'
        proyecto.save()
        return HttpResponseRedirect(reverse('proyecto:index'))
    return render(request, template_name, {'object':proyecto})


class SolicitarPermisosView(FormView):
    """ View de formulario de solicitud de permisos. Este view sierve un template con el formulario donde el usuario
    debe llenar el asunto el cuerpo de la solicitud.
    """
    template_name = "proyecto/solicitud_form.html"
    form_class = PermisoSolicitudForm
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        """ Función que controla que el proyecto es activo, si no, vuelve a la ruta anterior. """
        proyecto = get_object_or_404(Proyecto,pk=self.kwargs['pk_proy'])
        next = request.GET.get('next')
        if proyecto.estado_de_proyecto != 'A':
            messages.warning(request, '¡El proyecto fue finalizado, no se puede hacer cambios!')
            return HttpResponseRedirect(next)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Función que inyecta las variables de contexto que se utilizan en el template."""
        context = super(SolicitarPermisosView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
        })
        return context

    def form_valid(self,form):
        """ Función que envía el correo al scrum master del proyecto con la solicitud del usuario. """
        user = User.objects.get(pk=self.request.user.pk)
        proyecto = Proyecto.objects.get(id=self.kwargs['pk_proy'])
        send_mail(
            subject=form.cleaned_data['asunto'],
            message=form.cleaned_data['body'],
            from_email=user.email,
            recipient_list=[proyecto.owner.email]
        )
        return HttpResponseRedirect(reverse('proyecto:detail',kwargs={'pk':self.kwargs['pk_proy']}))


class AgregarSprintView(PermissionRequiredMixin, CreateView):
    """ View para agregar nuevos sprints. 
    En el form solo se puede indicar el tiempo de duración en días del sprint.
    """
    model = Sprint
    template_name = "proyecto/agregar_sprint.html"
    form_class = SprintCrearForm
    raise_exception = True
    permission_required = ('proyecto.p_administrar_sprint')

    def get_object(self):
        """Función que retorna el proyecto con el cual vamos a comprobar el permiso"""
        self.obj = get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])
        return self.obj

    def dispatch(self, request, *args, **kwargs):
        """ Función que controla que controla que el proyecto esté activo y que no haya sprint en planificación. 
        En caso de no cumplir vuelve a la ruta anterior.
        """
        sprint_count = Sprint.objects.filter(proyecto__id=self.kwargs['pk_proy']).filter(
            estado_de_sprint='I').count()
        proyecto = get_object_or_404(Proyecto,pk=self.kwargs['pk_proy'])
        next = request.GET.get('next')
        if proyecto.estado_de_proyecto != 'A':
            messages.warning(request, '¡El proyecto fue finalizado, no se puede hacer cambios!')
            return HttpResponseRedirect(next)
        if sprint_count != 0:
            messages.warning(request, 'No se puede agregar otro sprint, hay un sprint en planificación')
            return HttpResponseRedirect(next)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Función que inyecta las variables de contexto que se utilizan en el template."""
        context = super(AgregarSprintView,self).get_context_data(**kwargs)
        Sprints_count = Sprint.objects.filter(proyecto__id=self.kwargs['pk_proy']).exclude(estado_de_sprint='C').count()
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'count': Sprints_count + 1,
            'Sprint_count': Sprint.objects.filter(proyecto__id=self.kwargs['pk_proy']).filter(
            estado_de_sprint='I').count()

        })
        return context

    # def get_form_kwargs(self):
    #     """ Función que inyecta el id del proyecto como argumento. """
    #     kwargs = super(AgregarSprintView, self).get_form_kwargs()
    #     kwargs['pk_proy'] = self.kwargs['pk_proy']
    #     return kwargs

    def form_valid(self,form):
        """ Función que guarda el sprint nuevo. Agrega el nombre con la numeración correcta. Agrega el proyecto al sprint. """
        proyecto = Proyecto.objects.get(pk = self.kwargs['pk_proy'])
        Sprints_count = Sprint.objects.filter(proyecto__id=self.kwargs['pk_proy']).exclude(estado_de_sprint='C').count()
        obj = form.save(commit=True)
        obj.identificador = 'Sprint ' + str(Sprints_count+1)
        obj.proyecto = proyecto
        obj.save()
        return HttpResponseRedirect(reverse('proyecto:detail',kwargs={'pk':self.kwargs['pk_proy']}))


class EquipoSprintUpdateView(PermissionRequiredMixin,SingleObjectMixin,FormView):
    """ View para modificar el equipo del Sprint.
    Desde este view también se puede eliminar miembros del equipo.
    Devuelve un inset form.
    """
    model = Sprint
    template_name = 'proyecto/sprint_equipo_edit.html'
    raise_exception = True
    permission_required = ('proyecto.p_administrar_devs')
    
    def get_permission_object(self):
        """ Función que devuelve el proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

    def get_context_data(self, **kwargs):
        """ Función que inyecta las variables de contexto que se utilizan en el template."""
        context = super(EquipoSprintUpdateView,self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'Sprint': Sprint.objects.get(pk=self.kwargs['pk']),
        })
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(Sprint.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(Sprint.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """ Función que retorna el form """
        return EquipoFormset(**self.get_form_kwargs(),form_kwargs={'proyecto':self.kwargs['pk_proy']}, instance=self.object)

    def form_valid(self, form):
        """ Después de modificar el equipo del sprint se actualizan las horas disponibles del sprint"""
        form.save()
        sprint = Sprint.objects.get(pk=self.kwargs['pk'])
        equipo = ProyectUser.objects.filter(sprint__pk=sprint.pk)
        sprint.horas_disponibles = round(equipo.aggregate(Sum('horas_diarias')).get('horas_diarias__sum',0.00) * Decimal(sprint.duracionSprint),1)
        sprint.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Equipo del Sprint actualizado'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """ Función que retorna la ruta de éxito """
        return reverse('proyecto:sprint-detail', kwargs={'pk_proy': self.kwargs['pk_proy'],'sprint_id':self.kwargs['pk']})


class SprintUpdateView(PermissionRequiredMixin,UpdateView):
    """ View para modificar un Sprint. Se puede modificar la duración en días del sprint.
    Sólo será posible modificar el sprint si el sprint está en estado de inicialización o planificación.
    """
    model = Sprint
    form_class= SprintModificarForm
    template_name = 'proyecto/sprint_modificar.html'
    permission_required = ('proyecto.p_administrar_sprint')
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        """ Función que controla que el proyecto es activo y que el sprint está en estado de inicialización. Si
        no vuelve a la ruta anterior.
        """
        sprint = get_object_or_404(Sprint,pk=self.kwargs['sprint_id'])
        proyecto = get_object_or_404(Proyecto,pk=self.kwargs['pk_proy'])
        next = request.GET.get('next')
        if proyecto.estado_de_proyecto != 'A':
            messages.warning(request, '¡No se puede finalizar un proyecto que no es activo!')
            return HttpResponseRedirect(next)
        if sprint.estado_de_sprint != 'I':
            messages.warning(request, 'No se puede modificar un sprint que no está en estado de Inicializado')
            return HttpResponseRedirect(next)
        return super().dispatch(request, *args, **kwargs)

    def get_permission_object(self):
        """ Función que devuelve el proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

    def get_object(self, queryset=None):
        """ Función que devuelve el sprint a modificar"""
        id = self.kwargs['sprint_id']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        """ Función que inyecta las variables de context que serán utilizados en el template"""
        context = super(SprintUpdateView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'update': True,
        })
        return context

    def get_success_url(self):
        """ Función que devuelve la ruta de éxito """
        return reverse('proyecto:detail', kwargs={'pk': self.kwargs['pk_proy'],})


#Views de user story
@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
@permission_required_or_403('proyecto.p_aprobar_us',(Proyecto,'pk','pk_proy'))
def agregar_user_story_view(request, pk_proy):
    """
    Vista para agregar un user story al product backlog.
    Se toman como parámetros el nombre, la descripción y el tiempo estimado por el scrum master.
    """
    contexto = {}
    contexto.update({
        'proyecto_id': pk_proy
    })
    proyecto = get_object_or_404(Proyecto,pk=pk_proy)
    if proyecto.estado_de_proyecto != 'A':
        messages.warning(request, 'El proyecto fue finalizado, no se puede hacer cambios')
        return redirect('proyecto:product-backlog', pk_proy) 

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
            HistorialUS.objects.create(us_fk=get_object_or_404(UserStory, pk=u_story.pk), version=1, nombre=u_story.nombre, descripcion=u_story.descripcion, prioridad = u_story.prioridad_user_story)
            #Redirigimos al product backlog
            return redirect('proyecto:product-backlog', pk_proy)  
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_user_story_view.html', context=contexto)
    else:
        form = AgregarUserStoryForm()
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_user_story_view.html', context=contexto)


class UserStoryUdateView(PermissionRequiredMixin,UpdateView):
    """ View para modificar user storys no aprobados. """
    model = UserStory
    form_class= AgregarUserStoryForm
    template_name = 'proyecto/nuevo_user_story_view.html'
    raise_exception = True
    permission_required = ('proyecto.p_aprobar_us')
    raise_exception = True

    def get_permission_object(self):
        """ Función que devuelve el proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

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
        """ Función que retorna la ruta de éxito. """
        return reverse('proyecto:product-backlog', kwargs={'pk_proy': self.kwargs['pk_proy'],})

    def form_valid(self, form):
        """ Función que guarda los nuevos casos y guarda una nueva versión en el historial. """
        us = form.save()
        ver = HistorialUS.objects.filter(us_fk__id=us.pk).count()
        ver += 1
        HistorialUS.objects.create(us_fk=get_object_or_404(UserStory, pk=us.pk), version=ver, nombre=us.nombre, descripcion=us.descripcion, prioridad = us.prioridad_user_story)
        return HttpResponseRedirect(self.get_success_url())


class ProductBacklogView(PermissionRequiredMixin, ListView):
    """ View de todos los user storys del proyecto. A la izquierda se ven los user storys temporales, a la derecha los aprobados que ya se encuentran el backlog. """
    model = UserStory
    template_name = 'proyecto/product_backlog.html'
    permission_required = ('sso.pg_is_user','sso.pg_puede_acceder_proyecto')

    def get_context_data(self, **kwargs):
        """ Función para inyectar variables de contexto que serán utilizados en el template."""
        context = super(ProductBacklogView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'user_storys_nuevos': ProductBacklog.objects.get(proyecto__pk = self.kwargs['pk_proy']).userstory_set.filter(estado_aprobacion='T').exclude(estado_aprobacion='C'),
            'product_backlog': ProductBacklog.objects.get(proyecto__pk = self.kwargs['pk_proy']).userstory_set.filter(estado_aprobacion='A'),
        })
        return context


class AprobarUserStoryView(PermissionRequiredMixin,UpdateView):
    """ View de aprobación del user story.
    Al inicio cuando el user story es agregado al backlog, tiene estado temporal, en estado temporal se puede modificar el user story.
    Una vez que no se quiere modificar el user story, se lo aprueba y apartir de ahí no es editable.
    Muestra un template de confirmación de aprobación.
    """
    model = UserStory
    template_name = 'proyecto/userstory_aprobar_confirm.html'
    form_class= UserstoryAprobarForm
    raise_exception = True
    permission_required = ('proyecto.p_aprobar_us')

    def get_permission_object(self):
        """ Función que devuelve el user proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

    def dispatch(self, request, *args, **kwargs):
        """ Función que controla que el user story está en estado temporal, si no vuelve a la ruta anterior. """
        userstory = get_object_or_404(UserStory,pk=self.kwargs['us_id'])
        next = request.GET.get('next')
        if userstory.estado_aprobacion != 'T':
            messages.warning(request, 'No se puede aprobar un user story ya aprobado')
            return HttpResponseRedirect(next)
        return super().dispatch(request, *args, **kwargs)


    def get_object(self, queryset=None):
        """ Función que devuelve el user story a aprobar """
        id = self.kwargs['us_id']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        """ Función para inyectar variables de contexto que serán utilizados en el template."""
        context = super(AprobarUserStoryView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
        })
        return context

    def form_valid(self, form):
        """ Función que guarda el form y guarda el nuevo estado del user story. """
        userstory = form.save()
        userstory.estado_aprobacion = 'A'
        userstory.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """ Función que devuelve la ruta de éxito. """
        return reverse('proyecto:product-backlog', kwargs={'pk_proy': self.kwargs['pk_proy']})


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
        sprint = Sprint.objects.get(pk=self.kwargs['sprint_id'])

        if total_us == ready_us and total_us != 0:
            context.update({
                'ready_inicio': True
            })

        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'sprint': sprint,
            'user_storys': ProductBacklog.objects.get(proyecto__pk = self.kwargs['pk_proy']).userstory_set.filter(estado_aprobacion='A').filter(sprint__isnull=True),
            'sprint_backlog': sprint_backlog,
            'hours_remaining': sprint.horas_disponibles if sprint.horas_disponibles != None else 0 - sprint.carga_horaria,
            'owner': Proyecto.objects.get(pk=self.kwargs['pk_proy']).owner
        })
        return context


class UserStoryDetailView(UpdateView):
    """ 
    Vista para ver en detalle el user story. Es un updateview que será usado por el scrum master del proyecto y por el encargado asignado.
    Dependiendo de la persona que abre el link, se muestran los campos del form.
    Si el user story no está asignado a un sprint, se le deja estimar al scrum master, asignar un desarrollador y hace su estimación de tiempo.
    Cuando el scrum master le asignó un dev, se le envia un correo al dev y el dev tiene que estimar el tiempo de duración del user story (planning poker).
    TODO
    falta ver que permisos se requieren en este view
    """
    model = UserStory
    template_name = 'proyecto/userstory_detail_update.html'
    raise_exception = True

    def get_object(self, queryset=None):
        """ Función que retorna el user story"""
        id = self.kwargs['us_id']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        """ Función para inyectar variables de contexto que serán utilizados en el template.
        Hay varias variables que son inyectados dependiendo del estado del sprint, y dependiendo si el usuario es el scrum master o
        el encargado del user story.
        """
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
            'daily_list': Daily.objects.filter(user_story__pk=self.kwargs['us_id']).filter(sprint__pk=self.kwargs['sprint_id']),
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
        """ Función que hace calculos de promedio y envia un email al encargado, después de que se guardan los cambios del user story. 
        Cuando se asignó un user story a un dev, se asigna un permiso especial al encargado y al scrum master pero que ellos tengan permisos exclusivos
        sobre el user story. Ese permisos es necesario para administrar los dailys del user story y cambiar de estados en el Kanban.
        """
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
        if us.encargado:
            perm = Permission.objects.get(codename='us_manipular_userstory_dailys')
            assign_perm(perm,us.encargado.usuario,us)
            assign_perm(perm,proyecto.owner,us)


        tiempo = UserStory.objects.filter(sprint__id=self.kwargs['sprint_id']).aggregate(Sum('tiempo_promedio_calculado')).get('tiempo_promedio_calculado__sum',0.00)
        if tiempo != None:
            sprint.carga_horaria = tiempo
        else:
            sprint.carga_horaria = 0

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
            'historial' : HistorialUS.objects.filter(us_fk__pk = self.kwargs['us_id']).exclude(version = HistorialUS.objects.filter(us_fk__id=(self.kwargs['us_id'])).count()).order_by('-version'),
        })
        return context


@permission_required_or_403('proyecto.p_administrar_us',(Proyecto,'pk','pk_proy'))
@permission_required_or_403('proyecto.p_administrar_sprint',(Proyecto,'pk','pk_proy'))
def quitar_user_story_view(request, pk_proy, sprint_id, us_id, template_name='proyecto/quitar_userstory_sprint.html'):
    """ 
    View para desasignar un user story del sprint. 
    Cuando el usuario realmente lo quiere desasignar, se quitan las horas estimadas, el sprint y el encargado previamentes asignados.
    Esta acción solo se puede hacer cuando el sprint está en planifiación.
    Al quitar el user story se quitan también los permisos del encargado y del scrum master que tenían específicamente para ese user story.
    """
    us = get_object_or_404(UserStory, pk=us_id)
    sprint = get_object_or_404(Sprint, pk=sprint_id)
    proyecto = get_object_or_404(Proyecto,pk = pk_proy)

    if sprint.estado_de_sprint != 'I':
        messages.add_message(
            request,
            messages.warning,
            'No se puede quitar un user story de un sprint que no está en estado de inicialización.'
        )
        return HttpResponseRedirect(reverse('proyecto:sprint-detail',kwargs={'pk_proy':pk_proy,'sprint_id':sprint_id}))


    if request.method=='POST':
        perm = Permission.objects.get(codename='us_manipular_userstory_dailys')
        remove_perm(perm,us.encargado.usuario,us)
        remove_perm(perm,proyecto.owner,us)
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


@permission_required_or_403('proyecto.p_administrar_sprint',(Proyecto,'pk','pk_proy'))
def iniciar_sprint_view(request, pk_proy, sprint_id, template_name='proyecto/iniciar_sprint.html'):
    """ 
    View para iniciar un sprint. El botón solo será visible cuando todos los user storys asignados tienen tiempos estimados.
    NO es posible iniciar un Sprint en planificación si hay otro Sprint activo.
    """
    sprint = get_object_or_404(Sprint, pk=sprint_id)

    if request.method=='POST':
        running = Sprint.objects.filter(proyecto__pk=pk_proy).filter(estado_de_sprint='A').count()
        if running != 0:
            messages.warning(request, 'Hay un sprint corriendo, no se puede iniciar un nuevo sprint.')
        else:
            sprint.estado_de_sprint = 'A'
            sprint.fechaInicio = datetime.now()
            sprint.fechaFin = datetime.now()+timedelta(days=30)
            sprint.save()
        return HttpResponseRedirect(reverse('proyecto:sprint-detail',kwargs={'pk_proy':pk_proy,'sprint_id':sprint_id}))
    return render(request, template_name, {'proyecto_id':pk_proy, 'sprint_id':sprint_id})


class SprintKanbanView(TemplateView):
    """ 
    Vista del Tablero Kanban de un Sprint.
    Se muestran por el momento las tres columnas de Todo, Doing y Done.
    Por el momento todavia no se puede cambiar el estado de los user storys.
    En el columna de Done se muestran todos los User storys que fueron enviados a revisión y necesitan QA.
    De ahí el usuario con los permisoss de hacer QA puede selecionarlo y hacer los procedimientos de QA. 
    Si el user story está aprobado en QA, quedará en la columna de Done pero se muestra que ya está listo para release.
    """
    model = Sprint
    template_name = 'proyecto/sprint_kanban.html'

    def get_context_data(self, **kwargs):
        context = super(SprintKanbanView,self).get_context_data(**kwargs)
        sprint_backlog = UserStory.objects.filter(sprint__pk = self.kwargs['sprint_id'])
        us_todo = sprint_backlog.filter(estado_user_story='TD')
        us_doing = sprint_backlog.filter(estado_user_story='DG')
        us_done = sprint_backlog.exclude(estado_user_story='TD').exclude(estado_user_story='DG')
        us_qa = sprint_backlog.filter(estado_user_story='QA')

        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'sprint': Sprint.objects.get(pk=self.kwargs['sprint_id']),
            'ready_inicio': True,
            'us_todo': us_todo,
            'us_doing':us_doing,
            'us_done':us_done,
            'us_qa':us_qa,
            'testing':serialize('json',us_todo)
        })
        return context


@permission_required_or_403('proyecto.us_manipular_userstory_dailys',(UserStory,'pk','us_id'))
def mark_us_doing(request, pk_proy, sprint_id,us_id):
    """ 
    Vista, que marca como en proceso a un user story en el Kanban. Con este view se cambia el estado a Doing.
    Este view se usa para cambiar el estado de To-Do a Doing y solo puede ser hecho por el encargado del user story y
    por el scrum master.
    """
    us = get_object_or_404(UserStory, pk=us_id)
    us.estado_user_story = 'DG'
    us.save()
    return HttpResponseRedirect(reverse('proyecto:sprint-kanban',kwargs={'pk_proy':pk_proy,'sprint_id':sprint_id}))


@permission_required_or_403('proyecto.us_manipular_userstory_dailys',(UserStory,'pk','us_id'))
def mark_us_todo(request, pk_proy, sprint_id,us_id):
    """ 
    Vista, que marca como To-Do a un user story en el Kanban.
    Este view se usa para cambiar el estado de Doing a To-Do y solo puede ser hecho por el encargado del user story y
    por el scrum master.
    """
    us = get_object_or_404(UserStory, pk=us_id)
    us.estado_user_story = 'TD'
    us.save()
    return HttpResponseRedirect(reverse('proyecto:sprint-kanban',kwargs={'pk_proy':pk_proy,'sprint_id':sprint_id}))


@permission_required_or_403('proyecto.us_manipular_userstory_dailys',(UserStory,'pk','us_id'))
def mark_us_done(request, pk_proy, sprint_id,us_id):
    """ 
    Vista, que marca como DONE a un user story en el Kanban.
    Este view se usa para cambiar el estado de Doing a Done y solo puede ser hecho por el encargado del user story y
    por el scrum master. En la vista se marca al user story en estado de QA. Eso hace que en la columna de Done,
    se indica en el user story que falta hacer QA.
    """
    us = get_object_or_404(UserStory, pk=us_id)
    us.estado_user_story = 'QA'
    us.save()
    return HttpResponseRedirect(reverse('proyecto:sprint-kanban',kwargs={'pk_proy':pk_proy,'sprint_id':sprint_id}))


class FinalizarSprintView(PermissionRequiredMixin,UpdateView):
    """ 
    Este view se usa para finalizar un sprint. Se controla que el Sprint esté en estado Activo y que el proyecto esté activo.
    El view devuelve un template que se usa para pedir una confirmación de finalización del usuario.
    Si se finaliza el sprint y hay user storys que no fueron terminados, se les quita del sprint y se pone su prioridad en
    Emergencia. Se quita el encargado y el tiempo estimado de duración del user story.
    """
    model = Sprint
    template_name = 'proyecto/sprint_finalizar_confirm.html'
    form_class=SprintFinalizarForm
    raise_exception = True
    permission_required = ('proyecto.p_administrar_sprint')

    def get_permission_object(self):
        """ Función que devuelve el proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

    def dispatch(self, request, *args, **kwargs):
        """ Función que controla de antemano que el sprint y el proyecto estén activos, si no se vuelve a la ruta anterior. """
        sprint = get_object_or_404(Sprint,pk=self.kwargs['sprint_id'])
        proyecto = get_object_or_404(Proyecto,pk=self.kwargs['pk_proy'])
        next = request.GET.get('next')
        if proyecto.estado_de_proyecto != 'A':
            messages.warning(request, 'El proyecto fue finalizado, no se puede hacer cambios')
            return HttpResponseRedirect(next)
        if sprint.estado_de_sprint != 'A':
            messages.warning(request, 'No se puede finalizar un sprint que no es activo')
            return HttpResponseRedirect(next)
        return super().dispatch(request, *args, **kwargs)


    def get_object(self, queryset=None):
        """ Función que devuelve el sprint a finalizar """
        id = self.kwargs['sprint_id']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        """ Función para inyectar variables de contexto que serán utilizados en el template."""
        context = super(FinalizarSprintView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'sprint_id': self.kwargs['sprint_id'],
        })
        return context

    def form_valid(self, form):
        """ Función que se ejecuta después de que el usuario confirma que quiere finalizar el sprint.
        Se recorre todos los user storys del sprint y en el caso de que su estado no es Done, se aumenta la prioridad y son desasociados del sprint
        para poder tratados en sprints futuros.
        """
        sprint = form.save()
        sprint.estado_de_sprint = 'F'
        sprint.save()

        us = UserStory.objects.filter(sprint__pk=sprint.pk)
        for story in us:
            if story.estado_user_story != 'DN':
                story.estado_user_story = 'TD'
                story.prioridad_user_story = 'E'
                story.tiempo_estimado_scrum_master = None
                story.tiempo_estimado_dev = None
                story.encargado = None
                story.sprint = None
                story.last_estimated = story.tiempo_promedio_calculado
                story.tiempo_promedio_calculado = None
                story.save()


        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('proyecto:sprint-kanban', kwargs={'pk_proy': self.kwargs['pk_proy'],'sprint_id':self.kwargs['sprint_id'],})


class QaView(PermissionRequiredMixin,FormView):
    """ 
    Vista de QA.
    Esta vista devuelve un form donde la persona con los permisos necesarios puede ver el user story en cuestión, puede llenar un comentario,
    y debe elegir si quiere aprobar el user story o si se lo devuelve al estado de Doing.
    En ambos casos se envia un correo al encargado del user story con el comentario hecho.
    """
    form_class=QaForm
    template_name = 'proyecto/qa_form.html'
    permission_required = ('proyecto.p_administrar_us_qa')
    raise_exception = True

    def get_permission_object(self):
        """ Función que devuelve el proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

    def dispatch(self, request, *args, **kwargs):
        """ 
        Función que revisa si el user story a revisar realmente tiene estado de QA. Si no, vuelve a la url anterior.
        """
        us = get_object_or_404(UserStory, pk=self.kwargs['us_id'])
        proyecto = get_object_or_404(Proyecto,pk=self.kwargs['pk_proy'])
        next = request.GET.get('next')
        if proyecto.estado_de_proyecto != 'A':
            messages.warning(request, 'El proyecto fue finalizado, no se puede hacer cambios')
            return HttpResponseRedirect(next)
        if us.estado_user_story != 'QA':
            messages.warning(request, 'No se puede hacer Qa de un user story que no fue enviado para QA.')
            return HttpResponseRedirect(next)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Inyecta el user story, proyecto_id, sprint y sprint_id en el contexto del template."""
        context = super(QaView,self).get_context_data(**kwargs)
        context.update({
            'user_story': get_object_or_404(UserStory,pk=self.kwargs['us_id']),
            'proyecto_id': self.kwargs['pk_proy'],
            'sprint': get_object_or_404(Sprint,pk=self.kwargs['sprint_id']),
            'sprint_id': self.kwargs['sprint_id'],
        })
        return context
    
    def form_valid(self,form):
        """ 
        Si el form es válido, se verifica si el usuario eligió aprovar el user story o si no pasó el proceso de qa.
        Si fue aprovado se cambia el estado de 'QA' a 'DONE' y se le envia un correo al desarrollador.
        Si no pasa el qa, se cambia el estado de 'QA' a 'DOING' y se le envia un correo al desarrollador.
        """
        if 'aprove' in self.request.POST:
            proyecto = get_object_or_404(Proyecto,pk=self.kwargs['pk_proy'])
            us = get_object_or_404(UserStory, pk=self.kwargs['us_id'])
            if self.request.POST['aprove'] == 'aproved':
                us.estado_user_story = 'DN'
                us.save()
                send_mail(
                    subject='El user story ' + us.nombre + ' fue aprovado',
                    message=form.cleaned_data['comentario'],
                    from_email=proyecto.owner.email,
                    recipient_list=[us.encargado.usuario.email]
                )
            elif self.request.POST['aprove'] == 'denied':
                us.estado_user_story = 'DG'
                us.save()
                send_mail(
                    subject='El user story ' + us.nombre + ' no pasó el QA',
                    message=form.cleaned_data['comentario'],
                    from_email=proyecto.owner.email,
                    recipient_list=[us.encargado.usuario.email]
                )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """ Función que devuelve la ruta de éxito. """
        return reverse('proyecto:sprint-kanban', kwargs={'pk_proy': self.kwargs['pk_proy'],'sprint_id':self.kwargs['sprint_id']})


class FinalizarProyectoView(PermissionRequiredMixin,UpdateView):
    """ 
    View para finalizar un proyecto.
    De antemano se controla que el estado del proyecto es Activo, se controla que todos los sprints fueron finalizados y que no haya user storys
    en el backlog que no fueron terminados. Si alguna de esas condiciones falla, no se puede finalizar el proyecto.
    El view devuelve un template de confirmación de finalización del proyecto.
    """
    model = Proyecto
    template_name = 'proyecto/proyecto_finalizar_confirm.html'
    form_class=ProyectoFinalizarForm
    raise_exception = True
    permission_required = ('proyecto.p_finalizar_proyectos')

    def get_permission_object(self):
        """ Función que devuelve el proyecto sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(Proyecto, pk = self.kwargs['pk_proy'])

    def dispatch(self, request, *args, **kwargs):
        """ Función que hacer el control preliminar del estado del proyecto, de los sprints y de los user storys. En el caso de fallar una
        de esas condiciones se vuelve a la ruta anterior.
        """
        proyecto = get_object_or_404(Proyecto,pk=self.kwargs['pk_proy'])
        next = request.GET.get('next')
        if proyecto.estado_de_proyecto != 'A':
            messages.warning(request, '¡No se puede finalizar un proyecto que no es activo!')
            return HttpResponseRedirect(next)
        elif Sprint.objects.filter(proyecto__pk=self.kwargs['pk_proy']).count() != Sprint.objects.filter(proyecto__pk=self.kwargs['pk_proy']).filter(estado_de_sprint='F').count():
            messages.error(request, '¡No se puede finalizar un proyecto que tiene sprints que no fueron finalizados!')
            return HttpResponseRedirect(next)
        elif ProductBacklog.objects.get(proyecto__pk=self.kwargs['pk_proy']).userstory_set.filter(estado_aprobacion='A').exclude(estado_user_story='DN').count() != 0:
            messages.error(request, '¡No se puede finalizar un proyecto que tiene user storys en el product backlog que no fueron completados!')
            return HttpResponseRedirect(next)

        return super().dispatch(request, *args, **kwargs)


    def get_object(self, queryset=None):
        """ Función que retorna el proyecto a finalizar """
        id = self.kwargs['pk_proy']
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        """ Función para inyectar variables de contexto que serán utilizados en el template."""
        context = super(FinalizarProyectoView, self).get_context_data(**kwargs)
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
        })
        return context

    def form_valid(self, form):
        """ Función que se ejecuta después de que el usuario confirmó que quiere finalizar el proyecto. """
        proyecto = form.save()
        proyecto.estado_de_proyecto = 'F'
        proyecto.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """ Función que devuelve la ruta de éxito, después de finalizar el proyecto. """
        return reverse('proyecto:detail', kwargs={'pk': self.kwargs['pk_proy']})


class SprintBurndownchartView(TemplateView):
    """ 
    Vista del burndownchart de un sprint. Se usa la librería de chart.js en el template para graficar el user story.
    Calcula el trabajo restante por día en el sprint hasta la fecha actual.
    TODO 
    Necesita revisión ya que parece que las fechas no funcionan correctamente.
    """
    template_name='proyecto/sprint_burndownchart.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        """ Función que inyecta los datos necesarios para el burndownchart.
        Se hace le cálculo de horas de trabajo restantes por día.
        """
        context = super(SprintBurndownchartView,self).get_context_data(**kwargs)
        sprint = get_object_or_404(Sprint,pk=self.kwargs['sprint_id'])
        fecha = sprint.fechaInicio
        work_left = []
        hours = sprint.carga_horaria
        today = datetime.now()

        for index in range(sprint.duracionSprint):
            hours_worked = Daily.objects.filter(sprint__pk=self.kwargs['sprint_id']).filter(fecha=fecha).aggregate(Sum('duracion')).get('duracion__sum',0.00) 
            if hours_worked == None:
                hours_worked = 0
            hours -= hours_worked
            if hours != None and hours >= 0:
                work_left.append(str(hours))
            else:
                work_left.append(str(0))

            fecha += timedelta(days=1)
            if fecha > today.date():
                break

        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'sprint': sprint,
            'sprint_id': self.kwargs['sprint_id'],
            'sprint_json': json.dumps(work_left),
            'dias': json.dumps(sprint.duracionSprint)
        })
        return context


@permission_required('sso.pg_is_user', return_403=True, accept_global_perms=True)
def userstory_cancelar(request, pk_proy, us_id, template_name='proyecto/userstory_cancelar.html'):
    """
    Este view se usa para quitar user storys del Backlog.
    Se accede desde la pantalla de editar un user story. Si se cancela, su estado es Cancelado y no será visible en el listado
    de user storys que se pueden agregar al Product backlog.
    """
    userstory = get_object_or_404(UserStory, pk=us_id)
    if request.method == 'POST':
        userstory.estado_aprobacion = 'C'
        userstory.save()
        return HttpResponseRedirect(reverse('proyecto:product-backlog', kwargs={'pk_proy': pk_proy}))
    return render(request, template_name, {'object': userstory, 'proyecto_id':pk_proy})


@permission_required_or_403('proyecto.us_manipular_userstory_dailys',(UserStory,'pk','us_id'))
def agregar_daily_view(request, pk_proy, sprint_id, us_id):
    """
    Vista para agregar un daily.
    Se toman como parámetros la descripción, un comentario de impedimientos, la comentario de progreso.
    El template es un form donde el usuario entra esos datos.
    La duración describida aquí es la información que influye en los datos del burndownchart del sprint. Donde por 
    día se resta los dailys del día del total de horas restantes.
    """
    sprint = get_object_or_404(Sprint,pk=sprint_id)
    userstory = get_object_or_404(UserStory,pk=us_id)
    contexto = {}
    contexto.update({
        'proyecto_id': pk_proy,
        'sprint': sprint,
        'sprint_id': sprint_id,
        'user_story': userstory
    })
    if request.method == 'POST':      
        form = DailyForm(request.POST or None)
        #Si el form se cargó correctamente, lo guardamos
        if form.is_valid():
            daily = form.save()
            daily.user_story = userstory
            daily.sprint = sprint
            daily.fecha = datetime.now()
            daily.save()
            #Redirigimos al daily
            return HttpResponseRedirect(reverse('proyecto:userstory-add-daily',kwargs={'pk_proy':pk_proy,'sprint_id':sprint_id, 'us_id':us_id})) 
        contexto['form'] = form
        return render(request, 'proyecto/daily_view_form.html', context=contexto)
    else:
        form = DailyForm()
        contexto['form'] = form
        return render(request, 'proyecto/daily_view_form.html', context=contexto)


class EditDailyView(PermissionRequiredMixin,UpdateView):
    """
    Vista para editar un Daily
    Sierve un template de formulario donde el usuario puede modificar los campos del daily.
    """
    model = Daily
    permission_required = ('proyecto.us_manipular_userstory_dailys')
    template_name = 'proyecto/daily_view_form.html'
    form_class= DailyForm
    raise_exception = True

    def get_permission_object(self):
        """ Función que devuelve el user story sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(UserStory, pk = self.kwargs['us_id'])

    def get_object(self, queryset=None):
        """ Función que retorna el daily que va ser modificado """
        d_pk = self.kwargs['d_pk']
        return self.model.objects.get(pk = d_pk)

    def get_context_data(self, **kwargs):
        """ Función que inyecta todos las variables de contexto que se necesitan en el template. """
        context = super(EditDailyView,self).get_context_data(**kwargs)
        sprint = get_object_or_404(Sprint,pk=self.kwargs['sprint_id'])
        userstory = get_object_or_404(UserStory,pk=self.kwargs['us_id'])

        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'user_story': userstory,
            'edit': True,
            'sprint': sprint,
            'sprint_id': self.kwargs['sprint_id'],
        })
        return context


    def form_valid(self, form):
        """
        En esta función se guarda los cambios hechos.
        """
        form.save()
        return HttpResponseRedirect(reverse('proyecto:editar-daily',kwargs={'pk_proy':self.kwargs['pk_proy'],'sprint_id':self.kwargs['sprint_id'], 'us_id':self.kwargs['us_id']}))


class EliminarDailyView(PermissionRequiredMixin,DeleteView):
    """
    Este View es un DeleteView para facilitar la eliminación de un registro de Daily.
    Este View requiere el permiso de manipular dailys de este user story.
    El template que se muestra es una pantalla de confirmación de eliminación del daily.
    """
    model = Daily
    template_name = 'proyecto/eliminar_daily_confirm.html'
    permission_required = ('proyecto.us_manipular_userstory_dailys')
    raise_exception = True

    def get_permission_object(self):
        """ Función que devuelve el user story sobre el cual se controlan si el usuario tiene permisos adecuados para este view """
        return get_object_or_404(UserStory, pk = self.kwargs['us_id'])

    def get_object(self, queryset=None):
        """ Función que retorna el daily que va ser eliminado"""
        d_pk = self.kwargs['d_pk']
        return self.model.objects.get(pk = d_pk)

    def get_context_data(self, **kwargs):
        """ Función que inyecta todas las variables de contexto necesarias en el template """
        context = super(EliminarDailyView, self).get_context_data(**kwargs)
        sprint = get_object_or_404(Sprint,pk=self.kwargs['sprint_id'])
        userstory = get_object_or_404(UserStory,pk=self.kwargs['us_id'])
        context.update({
            'proyecto_id': self.kwargs['pk_proy'],
            'sprint': sprint,
            'sprint_id': self.kwargs['sprint_id'],
            'user_story': userstory,
        })
        return context

    def form_valid(self, form):
        """ Función que guarda el form de eliminación """
        form.save()
        return HttpResponseRedirect(self.get_success_url(self.kwargs['pk_proy']))


    def get_success_url(self,**kwargs):
        """ Función que retorna a la ruta de éxito. """
        return reverse_lazy('proyecto:eliminar-daily',kwargs={'pk_proy':self.kwargs['pk_proy'],'sprint_id':self.kwargs['sprint_id'], 'us_id':self.kwargs['us_id']})