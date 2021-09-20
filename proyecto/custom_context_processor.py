from .models import Proyecto
from sso.models import User

def proyect_renderer(request):
    if request.user.is_authenticated == True:
        resp = {}
        resp['mis_proyectos'] = User.objects.get(id=request.user.id).proyecto_set.all().exclude(estado_de_proyecto='C') | Proyecto.objects.filter(owner_id=request.user.id).exclude(estado_de_proyecto='C')
        return resp
    else:
        return Proyecto.objects.none()