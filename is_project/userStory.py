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