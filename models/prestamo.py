class Prestamo:
    def __init__(self, id, usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion):
        self.id = id
        self.usuario_id = usuario_id
        self.libro_isbn = libro_isbn
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.fecha_devolucion = fecha_devolucion

    def __str__(self):
        return f"Prestamo(ID: {self.id}, Usuario ID: {self.usuario_id}, Libro ISBN: {self.libro_isbn}, " \
               f"Fecha Préstamo: {self.fecha_prestamo}, Fecha Devolución: {self.fecha_devolucion}, " \
               f"Fecha Devolución: {self.fecha_devolucion})"
