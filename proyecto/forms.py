from django.forms import fields
from proyecto.models import RolProyecto
from django.contrib.auth.models import Permission
from django import forms
from .models import Proyecto
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


class ProyectoForm(forms.ModelForm):
    """
    Form de proyecto que recibe los parámetros asociados al nombre, duración del sprint, fecha de incio y fin
    y el equipo encargado del proyecto.
    """
    class Meta:
        model = Proyecto
        fields = ["nombreProyecto", "duracionSprint", "fechaInicio", "fechaFin", "equipo"]

    
    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['equipo'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                            choices=[(p.id, p.first_name) for p in User.objects.all() if 
                                                               p.has_perm('sso.pg_is_user')     
                                                            ])



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
