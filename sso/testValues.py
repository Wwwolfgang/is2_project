import django.db
import pytest
from django.test import TestCase
import sso
from sso import models
from sso.tests import testDescripcionUserStory
from sso.tests import testListaParticipantes
from sso.tests import testComentarios
import datetime
def testExamples():
    comentario1 = sso.models.comentario("0001","0001","0001","Primer comentario",datetime.date.today())
    comentario2 = sso.models.comentario("0002","0001","0001","Segundo comentario",datetime.date.today())
    comentario3 = sso.models.comentario("0003","0001","0001","Tercer comentario",datetime.date.today())
    comentario4 = sso.models.comentario("0004","0001","0001","Cuarto comentario",datetime.date.today())
    comentario5 = sso.models.comentario("0005","0001","0001","Quinto comentario",datetime.date.today())
    comentario6 = sso.models.comentario("0006","","","",datetime.date.today())
    userStory1  = sso.models.userStory("Prueba","0001",["Cesar Rodas","Julio Lezcano"],"Primer User Story",0,[comentario1,comentario2,comentario3,comentario4,comentario5],20,10)
    userStory2  = sso.models.userStory("Prueba 2","0002",["Roberto Rodriguez","Julio Lezcano"],"Segundo User Story",0,[comentario6],20,10)
    assert testDescripcionUserStory(userStory1) == True
    assert testDescripcionUserStory(userStory2) == True
    assert testListaParticipantes(userStory1) == True
    assert testListaParticipantes(userStory2) == True
    assert testComentarios(userStory1) == True 
    #assert testComentarios(userStory2) == True