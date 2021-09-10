""" 
Listado de urls de la app sso.
Todas las rutas tienen un prefijo /administration/

- la ruta inicial /administration/ nos lleva a la página de Administración con un listado de los roles de sistema y los usuarios del sistema. Desde aquí el administrador puede asignar roles, etc.
- /administration/<pk>/update-rol-sistema direcciona a un Form para modificar permisos de roles.
- /administration/<pk>/asignar-rol-sistema direcciona a un Form para asignar roles a un usuario.
- /administration/<pk>/delete-user direcciona a un Form para confirmar la debaja del usuario.
- /administration/<pk>/update-user direcciona a un Form para modificar un usuario p.E. su estado de Administrador.
"""

from django.urls import path
from .views import ListaRolesSistema, DeleteUser, UpdateUser, UpdateRolSistema,UserAssignSisRole,enviar_solicitud_accesso_view,SolicitarPermisosView
from django.views.generic import TemplateView

app_name = 'sso'

urlpatterns = [
    path('', ListaRolesSistema.as_view(), name='roles-sistema-listado'),
    path('<pk>/update-rol-sistema', UpdateRolSistema.as_view(), name='rol-sistema-update'),
    path('<pk>/asignar-rol-sistema', UserAssignSisRole.as_view(), name='rol-sistema-asignar'),
    path('<pk>/delete-user',DeleteUser.as_view(), name='user-delete'),
    path('<pk>/update-user',UpdateUser.as_view(), name='user-update'),
    path('<pk>/enviar-solicitud/',enviar_solicitud_accesso_view,name='solicitar-accesso'),
    path('<user_id>/solicitud-permisos/',SolicitarPermisosView.as_view(),name='solicitud-permisos'),
    
]