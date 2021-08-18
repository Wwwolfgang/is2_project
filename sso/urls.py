from django.urls import path
from .views import ListaRolesSistema
from django.views.generic import TemplateView


app_name = 'sso'

urlpatterns = [
    path('', ListaRolesSistema.as_view(), name='roles-sistema-listado'),
    
]