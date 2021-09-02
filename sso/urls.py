from django.urls import path
from .views import ListaRolesSistema, DeleteUser, UpdateUser, UpdateRolSistema,UserAssignSisRole
from django.views.generic import TemplateView


app_name = 'sso'

urlpatterns = [
    path('', ListaRolesSistema.as_view(), name='roles-sistema-listado'),
    path('<pk>/update-rol-sistema', UpdateRolSistema.as_view(), name='rol-sistema-update'),
    path('<pk>/asignar-rol-sistema', UserAssignSisRole.as_view(), name='rol-sistema-asignar'),
    path('<pk>/delete-user',DeleteUser.as_view(), name='user-delete'),
    path('<pk>/update-user',UpdateUser.as_view(), name='user-update')
    
]