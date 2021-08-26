from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto
from .forms import ProyectoForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.urls import reverse

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
    form = ProyectoForm(request.POST or None)
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
