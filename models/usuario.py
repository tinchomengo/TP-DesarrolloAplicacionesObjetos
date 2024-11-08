class Usuario:
    def __init__(self, id, nombre, apellido, tipo_usuario, direccion, telefono):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_usuario = tipo_usuario
        self.direccion = direccion
        self.telefono = telefono

    def __str__(self):
        return (f"Usuario({self.id}, {self.nombre}, {self.apellido}, Tipo: {self.tipo_usuario}, "
                f"Dirección: {self.direccion}, Teléfono: {self.telefono})")
