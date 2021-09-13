#import django.db
import pytest
#from django.test import TestCase
from proyecto.models import userStory
from proyecto.models import comentario
import datetime
def testNombreUserStory():
    nombreUserStory = "0001"
    isNumber = '0123456789'
    isSymbol = '!@#$%^&*()'
    for i in range (10):
        for j in range( nombreUserStory.__len__() ):
            assert isNumber[i] != nombreUserStory[j] or isSymbol[i] != nombreUserStory[j]

def testDescripcionUserStory(userStoryPrueba : userStory):
    assert userStoryPrueba.descripcionUserStory != ""

def testComentarios(userStoryPrueba : userStory):
    assert "" not in comentario.codComentario.all() or comentario.codUserStory.all()

def testListaParticipantes(userStoryPrueba: userStory):
    assert "" not in userStoryPrueba.listaParticipantes.all()

@pytest.mark.django_db
def testTiempoEmpleado():
    tiempoEmpleado = 10
    assert tiempoEmpleado >= 0 and tiempoEmpleado <= 30
    comentario1 = comentario(codComentario = "0001",codUserStory = "0001",codProyecto = "0001",descripcion = "Primer comentario",fecha = datetime.date.today())
    comentario2 = comentario(codComentario = "0002",codUserStory = "0002",codProyecto = "0002",descripcion = "Segundo comentario",fecha = datetime.date.today())
    comentario3 = comentario(codComentario = "0003",codUserStory = "0003",codProyecto = "0003",descripcion = "Tercer comentario",fecha = datetime.date.today())
    comentario4 = comentario(codComentario = "0004",codUserStory = "0004",codProyecto = "0004",descripcion = "Cuarto comentario",fecha = datetime.date.today())
    comentario5 = comentario(codComentario = "0005",codUserStory = "0005",codProyecto = "0005",descripcion = "Quinto comentario",fecha = datetime.date.today())
    comentario6 = comentario(codComentario = "0006",codUserStory = "",codProyecto = "",descripcion = "",fecha = datetime.date.today())
    comentario1.save()
    comentario2.save()
    comentario3.save()
    comentario4.save()
    comentario5.save()
    comentario6.save()

    userStory1  = userStory(nombreUserStory = "Prueba"  ,codigoUserStory = "0001",descripcionUserStory = "Primer User Story" ,estado = 0,estimacion = 20,tiempoEmpleado = 10)
    userStory2  = userStory(nombreUserStory = "Prueba 2",codigoUserStory = "0002",descripcionUserStory = "Segundo User Story",estado = 0,estimacion = 20,tiempoEmpleado = 10)
    userStory1.save()
    userStory2.save()
    userStory1.comentarios.add(comentario1)
    userStory1.comentarios.add(comentario2)
    userStory1.comentarios.add(comentario3)
    userStory1.comentarios.add(comentario4)
    userStory1.comentarios.add(comentario5)
    userStory2.comentarios.add(comentario6)
    
    testDescripcionUserStory(userStory1)
    testDescripcionUserStory(userStory2)
    testListaParticipantes(userStory1)
    testListaParticipantes(userStory2)
    testComentarios(userStory1)
    testComentarios(userStory2)