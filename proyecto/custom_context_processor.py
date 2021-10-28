from .models import Proyecto
from sso.models import User

def proyect_renderer(request):
    if request.user.is_authenticated == True:
        resp = {}
        proyectos = User.objects.get(id=request.user.id).proyecto_set.exclude(estado_de_proyecto='C') | Proyecto.objects.filter(owner_id=request.user.id).exclude(estado_de_proyecto='C')
        resp['mis_proyectos'] = proyectos.distinct()
        return resp
    else:
        return Proyecto.objects.none()