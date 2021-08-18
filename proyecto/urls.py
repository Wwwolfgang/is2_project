from django.urls import path
from django.views.generic import TemplateView


app_name = 'proyecto'

urlpatterns = [
    path('', TemplateView.as_view(template_name="proyecto/index.html")),
    
]