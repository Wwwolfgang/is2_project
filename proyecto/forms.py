from proyecto.models import RolProyecto
from django.contrib.auth.models import Permission

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

