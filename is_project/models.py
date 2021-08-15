import datetime
class usuario:
    username = ""
    tokenSesion = False
    direccionCorreo = ""
    def crearProyecto():
        print("El proyecto fue creado.\n")
    def iniciarSistema():
        print("El sistema fue inicializado.\n")
    def cerrarSesion():
        print("Se cerro la sesion.\n")
class usuarioProyecto:
    codProyecto = ""
    rolUsuario = ""
    def cambiarRol(Self, username):
        Self.rolUsuario = username #?
    def solicitarCambioRol(Self):
        if( Self.rolUsuario == 1 ):
            return True
        return False
    def agregarUsuarioProyecto():
        print("Se agrego el usuario al proyecto")
    def asignarUserStory(Self,codUserStory, username):
        print("Se ha asignado el usuario al user story")
    def crearRolProyecto(Self,codProyecto, listaPermisos, descripcion):
        print("Se creo el rol")
    def crearUserStory(nombreUserStory, descripcionUserStory):
        print("El user story fue creado")
    def cambiarUserStory( descripcionUserStory ):
        print("El user story fue cambiado")
    def modificarEstadoUserStory(codUserStory, estado):
        print("El user story fue modificado")
    def crearSprint(nombreSprint, duracionSprint):
        print("El sprint fue creado")
class userStory:
    nombreUserStory = ""
    codigoUserStory = ""
    listaParticipantes = [""]
    descipcionUserStory = ""
    estado = 0
    #comentarios comentario[]
    estimacion = 0
    tiempoEmpleado = 0
    def obtenerNombre(Self):
        return Self.nombreUserStory
    def modificarNombre(Self, nombre):
        Self.nombreUserStory = nombre
    def actualizarEstado(Self, estado):
        Self.estado = estado
    def actualizarDescripcion(Self, descripcionUserStory):
        Self.descipcionUserStory = descripcionUserStory
    def agregarParticipantes(Self, participante):
        Self.listaParticipantes.append(participante)
    def eliminarParicipantes(Self, participante):
        for i in Self.listaParticipantes:
            if( i == participante ):
                Self.listaParticipantes.remove(participante)
                return True
        return False
    def actualizarHistorial():
        print("Se actualizo el historial")
    def generarEstimacion(int,int2):
        print("Se estima que el user story dure 1 mes")
class sprint:
    nombreSprint = ""
    codSprint = ""
    nroUserStories = 0
    #listaStories = userStory[]
    fechaInicio = datetime.date()
    fechaFin = datetime.date()
    duracionSprint = 0
    def modificarNombreSprint(self,nombreSprint):
        self.nombreSprint = nombreSprint
    #def agregarUserStory(self, nuevoUserStory):
    #   self.listaStories.append(nuevoUserStory)
    #   self.nroUserStories = self.nroUserStories + 1
    #def eliminarUserStory(self, codUserStory):
    #    if( codUserStory == self.listaStories ):
    #       eliminar()
    def actualizarFechaInicio(self):
        self.fechaInicio = datetime.date()
    def actualizarFechaFin(self):
        self.fechaFin = datetime.date()
    def terminarSprint():
        print("Se termino el sprint")
    def generarCodigoSprint(self):
        print("Se genero un codigo")
    def ingresarDuracionSprint(self,duracion):
        self.duracionSprint = duracion
    def actualizarDuracionSprint(self,duracion):
        print("Se actualizo la duracion de sprint")
class rol:
    nombreRol = ""
    claveProyecto = ""
    permisos = [""]
    def modificarRol(Self, nombreRol, permisos):
        Self.nombreRol = nombreRol
        Self.permisos = permisos
        print("Se modifico el rol")
    def obtenerNombreRol(Self):
        return Self.nombreRol
    def obtenerPermisos(Self):
        return Self.permisos
    def obtenerClave(Self):
        return Self.claveProyecto
#class kanban:
    #columnas = userStory[]
    #def moverUserStory(userStory codUserStory):
    #   print("Se movio el user story")
    #   return True
    #def asignarUserStory( username ):
    #   print("Se agrego al user story")
    #def actualizarKanban():
    #   print("Se actualizo el kanban")
    #def generarKanban(userStory[]):
    #def generarKanban(userStory listaStories):
    #   print("Se genero el kanban")
class historialCambiosUS:
    codHistorialCambios = ""
    codUserStory = ""
    codProyecto = ""
    codUsuario = ""
    descripcionCambio = ""
    fecha = datetime.date()
    def generarCambio(Self, descripcion, codProyecto, codUsuario, codUserStory):
        Self.codUserStory = codUserStory
        Self.codProyecto = codProyecto
        Self.codUsuario = codUsuario
        Self.descripcionCambio = descripcion
    def obtenerFecha(Self):
        return Self.fecha

class comentario:
    codComentario = ""
    codUserStory = ""
    codProyecto = ""
    descripcion = ""
    fecha = datetime.date()
    def generarCodComentario():
        print("Se genero comentario")
    def obtenerCodUserStory(self):
        return self.codUserStory
    def obtenerCodProyecto(self):
        return self.codProyecto
    def obtenerDescripcion(self):
        return self.descripcion
    def modificarDescripcion(self,descripcion):
        self.descripcion=descripcion
    def marcarFechaComentario(self):
        self.fecha = datetime.date()
    #def usuarioComentando(self, codUsuario):
    #   self.codComentario = codComentario
    #   Que hace esta funcion?

class burnDownChart:
    codBurnDownChart = ""
    codSprintRel = ""
    codProyRel = ""
    datosTeoricos = [0][0]
    datosReales = [2][0]
    def crearLineaTeorica( dificultadEstimadaTotal, totalDias ):
        print("Se creo la linea teorica")
    def actualizarLineaReal( storyPointsCompletado, dia ):
        print("Se actualizo la linea real")
    def dibujarBurnDownChart():
        print("Se dibujo el burn down chart")
    def borrarBurnDownChart():
        print("Se borro el burn down chart")

class proyecto:
    nombreProyecto = ""
    fechaInicio = datetime.date()
    fechaFin = datetime.date()
    codProyecto = ""
    estadoProyecto = 0
    nroSprints = 0
    #listaSprints = Sprint[]
    #listaUsuarios = Usuario[]
    #listaRoles = Rol[]
    def obtenerNombreProyecto(Self):
        return Self.nombreProyecto
    def obtenerFechaInicio(Self):
        return Self.fechaInicio
    def obtenerEstadoProyecto(Self):
        return Self.estadoProyecto
    def ingresarNombreProyecto(Self, nombreProyecto ):
        Self.nombreProyecto = nombreProyecto
    def finalizarProyecto(Self):
        print("Se finalizo el proyecto")
    def generarCodigoProyecto(Self):
        print("Codigo generado")
    def actualizarEstadoProyecto(Self, estadoProyecto ):
        Self.estadoProyecto = estadoProyecto
    #def agregarSprintProyecto(Self, sprintNuevo):
        #Self.listaSprints.add(sprintNuevo)
    def obtenerCantidadSprints(Self):
        return Self.nroSprints
    def marcarSprintTerminado(Self, codSprint):
        Self.estadoProyecto = codSprint
    #def actualizarBurnDownChart(self, dificultad):
        #Self