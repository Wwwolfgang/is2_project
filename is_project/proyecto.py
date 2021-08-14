import datetime
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