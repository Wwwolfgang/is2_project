import datetime
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