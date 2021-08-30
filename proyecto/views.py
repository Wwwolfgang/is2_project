from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto
from .forms import ProyectoForm
from django.views.generic import ListView, DetailView
from django.urls import reverse
from proyecto.forms import AgregarRolProyectoForm
from proyecto.models import RolProyecto
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import generic

class EliminarRolProyectoView(DeleteView):
    model = RolProyecto
    template_name = 'proyecto/eliminar_rol_proyecto.html'
    success_url = reverse_lazy('proyecto:roles')

class ListaRolProyectoView(generic.ListView):
    model = RolProyecto
    template_name = 'proyecto/lista_rol_proyecto.html'

class DetallesRolProyectoView(generic.DetailView):
    model = RolProyecto
    template_name = 'proyecto/detalles_rol_proyecto.html'


def agregar_rol_proyecto_view(request):
    contexto = {}
    if request.method == 'POST':
        form = AgregarRolProyectoForm(request.POST or None)
        #Si el form se cargó correctamente, lo guardamos
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('/home/proyecto/roles')  
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_rol_proyecto_view.html', context=contexto)
    else:
        form = AgregarRolProyectoForm()   
        contexto['form'] = form
        return render(request, 'proyecto/nuevo_rol_proyecto_view.html', context=contexto)

def editar_rol_proyecto_view(request, id_rol):
    rol = get_object_or_404(RolProyecto, pk=id_rol)
    contexto = {}
    if request.method == 'POST':
        form = AgregarRolProyectoForm(request.POST, instance=rol)

        if form.is_valid(): 
            rol = form.save()
            messages.success(request, 'Rol de proyecto actualizado exitosamente')
            return redirect('/home/proyecto/roles')
        contexto['form'] = form
        return render(request, 'proyecto/editar_rol_proyecto.html', context=contexto)
    else:
        form = AgregarRolProyectoForm(instance=rol, initial={'permisos': [r.id for r in rol.get_permisos()]})   
        contexto['form'] = form
        return render(request, 'proyecto/editar_rol_proyecto.html', contexto)


class IndexView(ListView):
    model = Proyecto
    template_name = 'proyecto/index.html'
    context_object_name = 'proyecto_list'
    queryset = Proyecto.objects.all()

    def get_queryset(self):
        return Proyecto.objects.all()


class ProyectoDetailView(DetailView):
    model = Proyecto
    template_name = 'proyecto/proyecto-detalle.html'

    def get_object(self, queryset=None):
        id = self.kwargs['pk']
        return self.model.objects.get(id=id)


def create(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('proyecto:index'))
    form = ProyectoForm()

    return render(request,'proyecto/create.html',{'form': form})

def edit(request, pk, template_name='proyecto/edit.html'):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    form = ProyectoForm(request.POST or None, instance=proyecto)
    if form.is_valid():
        form.save()
        return redirect('/home/proyecto')
    return render(request, template_name, {'form':form})

def delete(request, pk, template_name='proyecto/confirm-delete.html'):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method=='POST':
        proyecto.delete()
        return redirect('/home/proyecto')
    return render(request, template_name, {'object':proyecto})
