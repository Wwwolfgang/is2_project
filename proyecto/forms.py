from django.contrib.auth import models
from django.forms import fields, widgets
from django.contrib.auth.models import Permission
from django import forms
from .models import Proyecto, ProyectUser, RolProyecto, Sprint, UserStory, Daily
from sso.models import User
from django import forms
from django.forms.models import inlineformset_factory

class AgregarRolProyectoForm(forms.ModelForm):
    """
    Form para agregar un rol al proyecto.
    Se despliega la lista de permisos para que puedan seleccionarse los roles.
    """
    def __init__(self, *args, **kwargs):
        super(AgregarRolProyectoForm, self).__init__(*args, **kwargs)
        self.fields['permisos'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                            choices=[(p.id, p.name) for p in Permission.objects.all() if
                                                                     p.codename.startswith('p_') and not p.codename.startswith('pg_')])
    class Meta:
        model = RolProyecto
        fields = ['nombre','permisos']


class UserAssignRolForm(forms.ModelForm):
    """
    Form para asignar un rol a los participantes del proyecto.
    """
    class Meta:
        model = RolProyecto
        fields = ['participantes']
    
    def __init__(self, *args, **kwargs):
        proyecto_id = kwargs.pop('pk_proy',None)
        proyecto = Proyecto.objects.get(id=proyecto_id)
        super(UserAssignRolForm, self).__init__(*args, **kwargs)
        self.fields['participantes'] = CustomUserMCF(queryset= proyecto.equipo.all() | User.objects.filter(pk=proyecto.owner.pk),
        widget=forms.CheckboxSelectMultiple
    )


class CustomUserMCF(forms.ModelMultipleChoiceField):
    """ Un ModelMultipleChoiceField custom """
    def label_from_instance(self, member):
        return "%s" % member.first_name + " " + member.last_name


class ProyectoEditForm(forms.ModelForm):
    """
    Form de proyecto que recibe los parámetros asociados al nombre, duración del sprint, fecha de incio y fin
    y el equipo encargado del proyecto.
    """
    class Meta:
        model = Proyecto
        fields = ["nombreProyecto", "fechaInicio", "fechaFin"]




class ProyectoCreateForm(forms.ModelForm):
    """
    Form de proyecto que recibe los parámetros asociados al nombre, duración del sprint, fecha de incio y fin
    y el equipo encargado del proyecto.
    """
    class Meta:
        model = Proyecto
        fields = ["nombreProyecto", "fechaInicio", "fechaFin", "equipo"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user_id',None)
        user = User.objects.get(pk = user)
        super(ProyectoCreateForm,self).__init__(*args, **kwargs)
        self.fields['equipo'] = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(p.id, "%s" % p.first_name + " " + p.last_name) for p in User.objects.exclude(first_name__isnull=True).exclude(first_name__exact='').exclude(pk=user.pk) if p.has_perm('sso.pg_is_user')],
        required=False
    )

class ProyectoFinalizarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProyectoFinalizarForm, self).__init__(*args, **kwargs)
        self.fields['estado_de_proyecto'].required = False
    class Meta:
        model = Proyecto
        fields = ["estado_de_proyecto",]


class ImportarRolProyectoForm(forms.Form):
    """
    Form para importar roles de proyecto. Se seleccionan de entre todos los proyectos existentes
    en el sistema y se extraen sus roles para desplegarse en pantalla. 
    """
    class Meta:
        fields = ["roles"]

    def __init__(self, *args, **kwargs):
        proyecto_id = kwargs.pop('pk_proy',None)
        super(ImportarRolProyectoForm, self).__init__(*args, **kwargs)
        self.fields['roles'] = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(p.id, p.nombre) for p in RolProyecto.objects.exclude(proyecto__id=proyecto_id)]
    )


class AgregarParticipanteForm(forms.Form):
    """
    Form para agregar Participantes al Proyecto
    """
    class Meta:
        model = Proyecto
        fields = ['equipo']

    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('instance',None)
        super().__init__(*args, **kwargs)
        self.fields['equipo'] = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(p.id, "%s" % p.first_name + " " + p.last_name) for p in User.objects.exclude(first_name__isnull=True).exclude(first_name__exact='').exclude(pk=proyecto.owner.pk).exclude(proyecto__id=proyecto.pk) if p.has_perm('sso.pg_is_user')]
    )


class DesarrolladorCreateForm(forms.ModelForm):
    """ Form para administrar el equipo de desarrolladores de un sprint. """

    def __init__(self, *args, **kwargs):
        proyect_id = kwargs.pop('proyecto',None)
        proyecto = Proyecto.objects.get(pk=proyect_id)
        super().__init__(*args, **kwargs)
        self.fields['usuario'] = forms.ModelChoiceField(
            empty_label="Opciones",
            queryset=proyecto.equipo.all() | User.objects.filter(pk=proyecto.owner.pk),
        )
        self.fields['horas_diarias'].required = True
        self.fields['usuario'].required = True
    class Meta:
        model = ProyectUser
        fields = ['usuario','horas_diarias']


class PermisoSolicitudForm(forms.Form):
    """ Form para solicitar más permisos al owner del proyecto. """
    asunto = forms.CharField(label='Asunto de la solitud', max_length=100, required=True)
    body = forms.CharField(widget=forms.Textarea,label='Solicitud',help_text='Especifique, que tipo de acceso o permisos necesita. Explique que acciones quiere hacer.',required=True)


class SprintCrearForm(forms.ModelForm):
    """ Form utilizado para la creación de un sprint. Se llenan los campos duración del Sprint y fechafin """
    class Meta:
        model = Sprint
        fields = ['duracionSprint']


class SprintModificarForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['duracionSprint']

class SprintFinalizarForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SprintFinalizarForm, self).__init__(*args, **kwargs)
        self.fields['estado_de_sprint'].required = False
    class Meta:
        model = Sprint
        fields = ['estado_de_sprint']


class UserstoryAprobarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserstoryAprobarForm, self).__init__(*args, **kwargs)
        self.fields['estado_aprobacion'].required = False
    class Meta:
        model = UserStory
        fields = ['estado_aprobacion']


EquipoFormset = inlineformset_factory(Sprint, ProyectUser,fields=('usuario','horas_diarias',),form=DesarrolladorCreateForm,can_delete=True)
class AgregarUserStoryForm(forms.ModelForm):
    """
    Form para crear un user story
    """
    def __init__(self, *args, **kwargs):
        super(AgregarUserStoryForm, self).__init__(*args, **kwargs)
        self.fields['prioridad_user_story'] = forms.ChoiceField(
            widget= forms.RadioSelect,
            choices=[('B','Baja'),('A','Alta'),('M','Media'),('E','Emergencia')]
        )  

    class Meta:
        model = UserStory
        fields = ['nombre','descripcion','prioridad_user_story']


class UserStoryAssingForm(forms.ModelForm):
    """ Form utilizado por el scrum master para asignar un user story a un desarrollador y estimar el tiempo de completar el user story """
    def __init__(self, *args, **kwargs):
        sprint_id = kwargs.pop('sprint_id',None)
        sprint = Sprint.objects.get(pk=sprint_id)
        super().__init__(*args, **kwargs)
        self.fields['encargado'] = forms.ModelChoiceField(
            empty_label="Desarrollador",
            queryset=sprint.sprint_team.all(),
        )
        self.fields['tiempo_estimado_scrum_master'].required = True
    class Meta:
        model = UserStory
        fields = ['tiempo_estimado_scrum_master','encargado','tiempo_estimado_dev']


class UserStoryDevForm(forms.ModelForm):
    """ Form utilizado por el encargado asignado al user story para estimar el tiempo de duración de completar el user story """
    def __init__(self, *args, **kwargs):
        sprint_id = kwargs.pop('sprint_id',None)
        super().__init__(*args, **kwargs)
    class Meta:
        model = UserStory
        fields = ['tiempo_estimado_dev']


class QaForm(forms.Form):
    comentario = forms.CharField(widget=forms.Textarea,label='Comentario',help_text='De un comentario o recomendación.',required=True)
class DailyForm(forms.ModelForm):
    """
    Form para crear un Daily
    """
    def __init__(self, *args, **kwargs):
        super(DailyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Daily
        fields = ['duracion','impedimiento_comentario','progreso_comentario']
