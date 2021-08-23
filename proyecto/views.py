from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, DetailView,CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
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