from proyecto.models import RolProyecto
from django.contrib.auth.models import Permission
from django import forms
from .models import Proyecto
from sso.models import User
from django import forms

class AgregarRolProyectoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgregarRolProyectoForm, self).__init__(*args, **kwargs)
        self.fields['permisos'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                            choices=[(p.id, p.name) for p in Permission.objects.all() if
                                                                     p.codename.startswith('p_') and not p.codename.startswith('pg_')])
    class Meta:
        model = RolProyecto
        fields = ['nombre','permisos']


class UserAssignRolForm(forms.ModelForm):
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
    class Meta:
        model = Proyecto
        fields = ["nombreProyecto", "duracionSprint", "fechaInicio", "fechaFin", "equipo"]

    
    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['equipo'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                            choices=[(p.id, p.first_name) for p in User.objects.all() if 
                                                               p.has_perm('sso.pg_is_user')     
                                                            ])

