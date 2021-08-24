from django.http.response import Http404
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect

from proyecto.forms import AgregarRolProyectoForm
from proyecto.models import RolProyecto

from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import generic

class ActualizarRolProyectoVista(UpdateView):
    model = RolProyecto
    fields = '__all__'

class EliminarRolProyectoVista(DeleteView):
    model = RolProyecto
    success_url = reverse_lazy('roles')

class ListaRolProyectoView(generic.ListView):
    model = RolProyecto
    template_name = 'proyecto/lista_rol_proyecto_2.html'

#def detalles_rol_proyecto_view(request, primary_key):
#    rol = get_object_or_404(RolProyecto, pk=primary_key)
#    return render(request, 'proyecto/detalles_rol_proyecto.html', context={'rol': rol})

class DetallesRolProyectoView(generic.DetailView):
    model = RolProyecto
    template_name = 'proyecto/detalles_rol_proyecto.html'


def lista_rol_proyecto_view(request):
    context ={}
    context["dataset"] = RolProyecto.objects.all()
    return render(request, "proyecto/lista_rol_proyecto.html", context)

def agregar_rol_proyecto_view(request):
    contexto = {}
    if request.method == 'POST':
        form = AgregarRolProyectoForm(request.POST or None)
        #Si el form se cargó correctamente, lo guardamos
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('/proyecto/rol/listar')  
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_rol_proyecto_view.html', context=contexto)
    else:
        form = AgregarRolProyectoForm()   
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_rol_proyecto_view.html', context=contexto)

