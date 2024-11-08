class Libro:
    def __init__(self, isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible):
        self.isbn = isbn
        self.titulo = titulo
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.autor_id = autor_id
        self.cantidad_disponible = cantidad_disponible

    def __str__(self):
        return (f"Libro({self.isbn}, {self.titulo}, {self.genero}, {self.anio_publicacion}, "
                f"Autor ID: {self.autor_id}, Cantidad Disponible: {self.cantidad_disponible})")
