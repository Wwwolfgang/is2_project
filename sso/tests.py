#import django.db
import pytest
#from django.test import TestCase
from sso.models import userStory
import datetime
#@pytest.mark.postgresql

def testNombreUserStory( userStory ):
    
    isNumber = '0123456789'
    isSymbol = '!@#$%^&*()'
    for i in range (10):
        for j in range( userStory.obtenerNombreUserStory().__len__ ):
            if isNumber[i] == userStory.obtenerNombreUserStory()[j] or isSymbol[i] == userStory.obtenerNombreUserStory()[j] :
                return False
    return True

def testDescripcionUserStory( userStory ):
    if userStory.obtenerDescripcionUserStory() == "" :
        return False
    return True

def testComentarios( userStory ):
    for comentario in userStory.obtenerComentarios():
        if comentario.obtenerCodComentario() == "" or comentario.obtenerCodUserStory() == "":
            return False
    return True

def testListaParticipantes( userStory ):
    for participante in userStory.obtenerListaParticipantes():
        if participante == "" :
            return False
    return True

def testTiempoEmpleado( userStory ):
    if userStory.obtenerTiempoEmpleado() > 0 and userStory.obtenerTiempoEmpleado() < 30:
        return False
    return True