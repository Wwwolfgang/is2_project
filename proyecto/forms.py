from django.forms import fields
from django.contrib.auth.models import Permission
from django import forms
from .models import Proyecto, ProyectUser,RolProyecto
from sso.models import User
from django import forms

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
        self.fields['participantes'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                            choices=[(p.id, p.first_name) for p in proyecto.equipo.all()])


class CustomUserMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, member):
        return "%s" % member.first_name + " " + member.last_name


class ProyectoEditForm(forms.ModelForm):
    """
    Form de proyecto que recibe los parámetros asociados al nombre, duración del sprint, fecha de incio y fin
    y el equipo encargado del proyecto.
    """
    class Meta:
        model = Proyecto
        fields = ["nombreProyecto", "duracionSprint", "fechaInicio", "fechaFin", "equipo"]

    def __init__(self, *args, **kwargs):
        super(ProyectoEditForm,self).__init__(*args, **kwargs)
        owner = self.instance.owner
        self.fields['equipo'] = CustomUserMCF(queryset= User.objects.filter(proyecto__id=self.instance.pk).exclude(pk=owner.pk),
        widget=forms.CheckboxSelectMultiple
    )


class ProyectoCreateForm(forms.ModelForm):
    """
    Form de proyecto que recibe los parámetros asociados al nombre, duración del sprint, fecha de incio y fin
    y el equipo encargado del proyecto.
    """
    class Meta:
        model = Proyecto
        fields = ["nombreProyecto", "duracionSprint", "fechaInicio", "fechaFin", "equipo"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user_id',None)
        user = User.objects.get(pk = user)
        super(ProyectoCreateForm,self).__init__(*args, **kwargs)
        self.fields['equipo'] = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[(p.id, "%s" % p.first_name + " " + p.last_name) for p in User.objects.exclude(first_name__isnull=True).exclude(first_name__exact='').exclude(pk=user.pk) if p.has_perm('sso.pg_is_user')]
    )


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

    def __init__(self, *args, **kwargs):
        proyect_id = kwargs.pop('pk_proy',None)
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
    asunto = forms.CharField(label='Asunto de la solitud', max_length=100, required=True)
    body = forms.CharField(widget=forms.Textarea,label='Solicitud',help_text='Especifique, que tipo de acceso o permisos necesita. Explique que acciones quiere hacer.',required=True)
