#import django.db
import pytest
#from django.test import TestCase
from sso.models import userStory
from sso.models import comentario
import datetime
def testNombreUserStory():
    nombreUserStory = "0001"
    isNumber = '0123456789'
    isSymbol = '!@#$%^&*()'
    for i in range (10):
        for j in range( nombreUserStory.__len__() ):
            assert isNumber[i] != nombreUserStory[j] or isSymbol[i] != nombreUserStory[j]

def testDescripcionUserStory():
    descripcionUserStory="0001"
    assert descripcionUserStory != ""

def testComentarios():
    comentario1 = comentario(codComentario = "0001",codUserStory = "0001",codProyecto = "0001",descripcion = "Primer comentario",fecha = datetime.date.today())
    assert comentario1.obtenerCodComentario() != "" or comentario1.obtenerCodUserStory() != ""

def testListaParticipantes():
    listaParticipantes = ["Cesar Rodas","Julio Lezcano"]
    for participante in listaParticipantes:
        assert participante != ""

def testTiempoEmpleado():
    tiempoEmpleado = 10
    assert tiempoEmpleado >= 0 and tiempoEmpleado <= 30
    #comentario1 = sso.models.comentario(codComentario = "0001",codUserStory = "0001",codProyecto = "0001",descripcion = "Primer comentario",fecha = datetime.date.today())
    #comentario2 = sso.models.comentario(codComentario = "0002",codUserStory = "0002",codProyecto = "0002",descripcion = "Segundo comentario",fecha = datetime.date.today())
    #comentario3 = sso.models.comentario(codComentario = "0003",codUserStory = "0003",codProyecto = "0003",descripcion = "Tercer comentario",fecha = datetime.date.today())
    #comentario4 = sso.models.comentario(codComentario = "0004",codUserStory = "0004",codProyecto = "0004",descripcion = "Cuarto comentario",fecha = datetime.date.today())
    #comentario5 = sso.models.comentario(codComentario = "0005",codUserStory = "0005",codProyecto = "0005",descripcion = "Quinto comentario",fecha = datetime.date.today())
    #comentario6 = sso.models.comentario(codComentario = "0006",codUserStory = "",codProyecto = "",descripcion = "",fecha = datetime.date.today())
    #userStory1  = sso.models.userStory(nombreUserStory = "Prueba",codigoUserStory = "0001",listaParticipantes = ["Cesar Rodas","Julio Lezcano"],descripcionUserStory = "Primer User Story",estado = 0,comentarios = [comentario1,comentario2,comentario3,comentario4,comentario5],estimacion = 20,tiempoEmpleado = 10)
    #userStory2  = sso.models.userStory(nombreUserStory = "Prueba 2",codigoUserStory = "0002",listaParticipantes = ["Roberto Rodriguez","Julio Lezcano"],descripcionUserStory = "Segundo User Story",estado = 0,comentarios = [comentario6],estimacion = 20,tiempoEmpleado = 10)
    #assert testDescripcionUserStory(userStory1) == True
    #assert testDescripcionUserStory(userStory2) == True
    #assert testListaParticipantes(userStory1) == True
    #assert testListaParticipantes(userStory2) == True
    #assert testComentarios(userStory1) == True 
    #firefassert testComentarios(userStory2) == True