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