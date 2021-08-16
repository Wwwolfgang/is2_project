from django.test import TestCase
from sso import models
import datetime
def comprobarNombreUserStory( nombreUserStory: str ):
    isNumber = '0123456789'
    isSymbol = '!@#$%^&*()'
    for i in range (10):
        if( isNumber[i] in nombreUserStory or isSymbol[i] in nombreUserStory ):
            print("Nombre invalido\n")
            return False
    return True
def comprobarDescripcionUserStory( descripcionUserStory ):
    if( descripcionUserStory ):
        print("Error: descripcion vacia")
        return False
def comprobarComentarios( comentarios ):
    for comentario in comentarios:
        if( comentario.codComentario == '' ):
            print("Error: codigo invalido\n")
            return False
        if( comentario.codUserStory == '' ):
            print("Error: user story invalido\n")
        if( comentario.fecha > datetime.date.today ):
            print("Error: fecha invalida")
    return True
def comprobarListaParticipantes( listaParticipantes ):
    for participante in listaParticipantes:
        if( participante == '' ):
            print("Error: usuario sin nombre\n")
            return False
    return True
def comprobarTiempoEmpleado( tiempoEmpleado ):
    return ( tiempoEmpleado > 0 and tiempoEmpleado < 30)
# Create your tests here.
