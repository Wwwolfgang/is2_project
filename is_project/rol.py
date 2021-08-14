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