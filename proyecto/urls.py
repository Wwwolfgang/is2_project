from django.urls import path
from django.views.generic import TemplateView
from .views import ProyectoDetailView, edit, create, delete, IndexView

app_name = 'proyecto'

urlpatterns = [
    path('', TemplateView.as_view(template_name="proyecto/index.html"),name='home'),
    path('proyecto/', IndexView.as_view(), name='index'),
    path('proyecto/<int:pk>/', ProyectoDetailView, name='detail'),
    path('proyecto/edit/<int:pk>/', edit, name='edit'),
    path('proyecto/create/', create, name='create'),
    path('proyecto/delete/<int:pk>/', delete, name='delete'),
]