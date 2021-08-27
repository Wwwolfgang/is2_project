from django import forms
from .models import Proyecto
from sso.models import User

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ["nombreProyecto", "duracionSprint", "fechaInicio", "fechaFin", "equipo"]

