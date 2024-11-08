class Autor:
    def __init__(self, id, nombre, apellido, nacionalidad):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad

    def __str__(self):
        return f"Autor({self.id}, {self.nombre}, {self.apellido}, {self.nacionalidad})"
