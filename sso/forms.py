from django import forms
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.forms import UserChangeForm
from .models import User

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
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
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
