from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect


from proyecto.forms import AgregarRolProyectoForm
from proyecto.models import RolProyecto

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class ActualizarRolProyecto(UpdateView):
    model = RolProyecto
    fields = '__all__'

class EliminarRolProyecto(DeleteView):
    model = RolProyecto
    success_url = reverse_lazy('roles')


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

