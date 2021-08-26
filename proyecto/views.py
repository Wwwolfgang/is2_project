from django.core import exceptions
from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, DetailView,CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
<<<<<<< Updated upstream
from django.urls import reverse
from .models import RolSistema
from proyecto import models
from django.contrib import postgres
class participanteUserStory():
    """
        Accede a la base de datos de user story, extrae el user story que coincida
        con el codigoUserStory, se agrega el participante solicitado y guarda.
        Caso contrario retorna exceptionCodigoUserStoryNotFound
    """
    def agregarParticipante(codigo, nombreParticipante):
        try:
            queryUserStory = models.userStory.objects.filter(codigoUserStory = codigo )
            queryUserStory.listaParticipantes.add(nombreParticipante)
            queryUserStory.save()
        except:
            print("codigo no encontrado")

    def eliminarParticipantes(codigo):
        try:
            queryUserStory = models.userStory.objects.filter(codigoUserStory = codigo )
            queryUserStory.listaParticipantes.remove()
            queryUserStory.save()
        except:
            print("codigo no encontrado")
    def mostrarParticipantes():
        queryUserStory = models.userStory.objects.all()
        for query in queryUserStory:
            print( query.listaParticipantes )
=======
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
    queryset = Group.objects.all()

    def eliminar(userStory: userStory,codigo, nombreParticipante):
        try:
            query = userStory.objects.get(codigoUserStory = codigo)
            for participante in query.listaParticipantes:
                if( participante.__eq__(nombreParticipante) ):
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
>>>>>>> Stashed changes
