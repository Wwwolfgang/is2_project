from django.core import exceptions
from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, DetailView,CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import User, userStory
from django.contrib.auth.models import Group

class ListaParticipantes(UpdateView):
    """ 
    Lista 
    """
    model = userStory
    context_object_name = 'Participantes'
    template_name = 'proyecto/participantes.html'
    raise_exception = True
    queryset = userStory.objects.all()

    def eliminar(userStory: userStory,codigo, nombreParticipante):
        try:
            query = userStory.objects.get(codigoUserStory = codigo)
            for participante in query.listaParticipantes:
                if( participante.username.__eq__(nombreParticipante) ):
                    query.listaParticipantes.remove(participante)
                    userStory = query
                    userStory.objects.save()
                    return
            print("Participante no encontrado")
            return
        except:
            print("Codigo no encontrado")
        return

    def agregar(userStory: userStory,codigo, nombreParticipante):
        try:
            query = userStory.objects.get(codigoUserStory = codigo)
            query.listaParticipantes.append(nombreParticipante)
            userStory = query
            userStory.objects.save()
            return
        except:
            print("Codigo no encontrado")
        return
    def listar(userStory: userStory,codigo):
        try:
            query = userStory.objects.get(codigoUserStory = codigo)
            for participante in query.ListaParticipantes:
                print(participante)
            return
        except:
            print("Codigo no encontrado")
        return
