from sso.models import User
from proyecto.models import RolProyecto,Proyecto,ProductBacklog,ProyectUser,Sprint,UserStory,HistorialUS,Daily
User1 = User.objects.get(id=1)
User2 = User.objects.get(id=2)
User3 = User.objects.get(id=3)
User4 = User.objects.get(id=4)
User5 = User.objects.get(id=5)
RolProyecto1 = RolProyecto.objects.get(id=6)
RolProyecto2 = RolProyecto.objects.get(id=7)
RolProyecto3 = RolProyecto.objects.get(id=8)
RolProyecto4 = RolProyecto.objects.get(id=9)
RolProyecto5 = RolProyecto.objects.get(id=10)
Proyecto1 = Proyecto.objects.get(id=11)
Proyecto2 = Proyecto.objects.get(id=12)
Proyecto3 = Proyecto.objects.get(id=13)
Proyecto4 = Proyecto.objects.get(id=14)
Proyecto5 = Proyecto.objects.get(id=15)
ProyectUser1 = ProyectUser.objects.get(id=16)
ProyectUser2 = ProyectUser.objects.get(id=17)
ProyectUser3 = ProyectUser.objects.get(id=18)
ProyectUser4 = ProyectUser.objects.get(id=19)
ProyectUser5 = ProyectUser.objects.get(id=20)
ProductBacklog1 = ProductBacklog.objects.get(id=21)
ProductBacklog2 = ProductBacklog.objects.get(id=22)
ProductBacklog3 = ProductBacklog.objects.get(id=23)
ProductBacklog4 = ProductBacklog.objects.get(id=24)
ProductBacklog5 = ProductBacklog.objects.get(id=25)
Sprint1 = Sprint.objects.get(id=26)
Sprint2 = Sprint.objects.get(id=27)
Sprint3 = Sprint.objects.get(id=28)
Sprint4 = Sprint.objects.get(id=29)
Sprint5 = Sprint.objects.get(id=30)
UserStory1 = UserStory.objects.get(id=31)
UserStory2 = UserStory.objects.get(id=32)
UserStory3 = UserStory.objects.get(id=33)
UserStory4 = UserStory.objects.get(id=34)
UserStory5 = UserStory.objects.get(id=35)
HistorialUS1 = HistorialUS.objects.get(id=36)
HistorialUS2 = HistorialUS.objects.get(id=37)
HistorialUS3 = HistorialUS.objects.get(id=38)
HistorialUS4 = HistorialUS.objects.get(id=39)
HistorialUS5 = HistorialUS.objects.get(id=40)
Daily1 = Daily.objects.get(id=41)
Daily2 = Daily.objects.get(id=42)
Daily3 = Daily.objects.get(id=43)
Daily4 = Daily.objects.get(id=44)
Daily5 = Daily.objects.get(id=45)
Proyecto1.owner = User1
Proyecto2.owner = User2
Proyecto3.owner = User3
Proyecto4.owner = User4
Proyecto5.owner = User5
ProyectUser1.usuario = User1
ProyectUser2.usuario = User2
ProyectUser3.usuario = User3
ProyectUser4.usuario = User4
ProyectUser5.usuario = User5
UserStory1.creador = User1
UserStory2.creador = User2
UserStory3.creador = User3
UserStory4.creador = User4
UserStory5.creador = User5
RolProyecto1.proyecto=Proyecto1
RolProyecto2.proyecto=Proyecto2
RolProyecto3.proyecto=Proyecto3
RolProyecto4.proyecto=Proyecto4
RolProyecto5.proyecto=Proyecto5
Proyecto1.equipo_desarrollador.set(ProyectUser1.__iter__)
Proyecto2.equipo_desarrollador.set(ProyectUser2.__iter__)
Proyecto3.equipo_desarrollador.set(ProyectUser3.__iter__)
Proyecto4.equipo_desarrollador.set(ProyectUser4.__iter__)
Proyecto5.equipo_desarrollador.set(ProyectUser5.__iter__)
ProyectUser1.sprint=Sprint1
ProyectUser2.sprint=Sprint2
ProyectUser3.sprint=Sprint3
ProyectUser4.sprint=Sprint4
ProyectUser5.sprint=Sprint5
ProductBacklog1.proyecto=Proyecto1
ProductBacklog2.proyecto=Proyecto2
ProductBacklog3.proyecto=Proyecto3
ProductBacklog4.proyecto=Proyecto4
ProductBacklog5.proyecto=Proyecto5
Sprint1.proyecto=Proyecto1
Sprint2.proyecto=Proyecto2
Sprint3.proyecto=Proyecto3
Sprint4.proyecto=Proyecto4
Sprint5.proyecto=Proyecto5
UserStory1.encargado=ProyectUser1
UserStory2.encargado=ProyectUser2
UserStory3.encargado=ProyectUser3
UserStory4.encargado=ProyectUser4
UserStory5.encargado=ProyectUser5
UserStory1.sprint=Sprint1
UserStory2.sprint=Sprint2
UserStory3.sprint=Sprint3
UserStory4.sprint=Sprint4
UserStory5.sprint=Sprint5
UserStory1.product_backlog=ProductBacklog1
UserStory2.product_backlog=ProductBacklog2
UserStory3.product_backlog=ProductBacklog3
UserStory4.product_backlog=ProductBacklog4
UserStory5.product_backlog=ProductBacklog5
HistorialUS1.us_fk=UserStory1
HistorialUS2.us_fk=UserStory2
HistorialUS3.us_fk=UserStory3
HistorialUS4.us_fk=UserStory4
HistorialUS5.us_fk=UserStory5
Daily1.user_story=UserStory1
Daily2.user_story=UserStory2
Daily3.user_story=UserStory3
Daily4.user_story=UserStory4
Daily5.user_story=UserStory5
Daily1.sprint=Sprint1
Daily2.sprint=Sprint2
Daily3.sprint=Sprint3
Daily4.sprint=Sprint4
Daily5.sprint=Sprint5
User1.save()
User2.save()
User3.save()
User4.save()
User5.save()
RolProyecto1.save()
RolProyecto2.save()
RolProyecto3.save()
RolProyecto4.save()
RolProyecto5.save()
Proyecto1.save()
Proyecto2.save()
Proyecto3.save()
Proyecto4.save()
Proyecto5.save()
ProyectUser1.save()
ProyectUser2.save()
ProyectUser3.save()
ProyectUser4.save()
ProyectUser5.save()
ProductBacklog1.save()
ProductBacklog2.save()
ProductBacklog3.save()
ProductBacklog4.save()
ProductBacklog5.save()
Sprint1.save()
Sprint2.save()
Sprint3.save()
Sprint4.save()
Sprint5.save()
UserStory1.save()
UserStory2.save()
UserStory3.save()
UserStory4.save()
UserStory5.save()
HistorialUS1.save()
HistorialUS2.save()
HistorialUS3.save()
HistorialUS4.save()
HistorialUS5.save()
Daily1.save()
Daily2.save()
Daily3.save()
Daily4.save()
Daily5.save()