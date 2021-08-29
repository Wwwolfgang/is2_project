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
                                                                     p.codename.startswith('p_')])
    class Meta:
        model = RolProyecto
        fields = '__all__'

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ["nombreProyecto", "duracionSprint", "fechaInicio", "fechaFin", "equipo"]

