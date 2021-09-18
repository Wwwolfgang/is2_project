from django import forms
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.forms import UserChangeForm
from .models import User

class CustomUserMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, member):
        return "%s" % member.name
class UpdateRolSistemaForm(forms.ModelForm):
    """ 
    Form para actualizar los permisos de los roles. Ya que los roles de sistema serán predefinidos en el Admin de Django,
    aquí solo serán modificables los permisos.
    """
    class Meta:
        model = Group
        fields = ['permissions']
        
    # permissions = forms.ModelMultipleChoiceField(
    #     queryset=Permission.objects.filter(
    #     codename='custom_acceder_ususario'),
    #     widget=forms.CheckboxSelectMultiple
    # )
    def __init__(self, *args, **kwargs):
        """ Retorna un listado de permisos de los cuales el usuario puede elegir. """
        super(UpdateRolSistemaForm,self).__init__(*args, **kwargs)
        self.fields['permissions'] = CustomUserMCF(
        queryset= Permission.objects.filter(codename__startswith='pg_'),
        widget=forms.CheckboxSelectMultiple
        )

class UserAssignRolForm(UserChangeForm):
    """ 
    Form para asignar Roles de Sistema a un usuario.
    Se puede asignar uno o más roles de sistema a un usuario.
    """

    class Meta:
        model = User
        fields = ['groups']

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class PermisoSolicitudForm(forms.Form):
    asunto = forms.CharField(label='Asunto de la solitud', max_length=100, required=True)
    body = forms.CharField(widget=forms.Textarea,label='Solicitud',help_text='Especifique, que tipo de acceso o permisos necesita. Explique que acciones quiere hacer.',required=True)
