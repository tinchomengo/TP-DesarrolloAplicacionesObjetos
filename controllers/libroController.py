from database.conexionBDA import DbSingleton
from models.libro import Libro
from sqlite3 import IntegrityError

class LibroController:
    def __init__(self):
        self.db = DbSingleton()

from datetime import datetime

class LibroController:
    def __init__(self):
        self.db = DbSingleton()

    def registrar_libro(self, isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible):
        # Validar que el año no sea mayor al actual
        anio_actual = datetime.now().year
        if anio_publicacion > anio_actual:
            print(f"El año de publicación {anio_publicacion} no puede ser mayor al actual ({anio_actual}).")
            return "Año inválido"

        # Validar que la cantidad disponible sea mayor a 0
        if cantidad_disponible <= 0:
            print(f"La cantidad disponible ({cantidad_disponible}) debe ser mayor a 0.")
            return "Cantidad inválida"

        # Verificar si el ISBN ya existe
        query_verificar = "SELECT * FROM libros WHERE isbn = ?"
        if self.db.fetch_query(query_verificar, (isbn,)):
            print(f"El ISBN {isbn} ya existe en la base de datos.")
            return "ISBN duplicado"
        
        # Insertar el libro si las validaciones son correctas
        query_insertar = """
        INSERT INTO libros (isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)

        # Insertar en 'historicoLibros'
        query_insertar_historico = """
        INSERT INTO historicoLibros (isbn, titulo, genero, anio_publicacion, autor_id)
        VALUES (?, ?, ?, ?, ?)
        """
        params_historico = (isbn, titulo, genero, anio_publicacion, autor_id)

        try:
            self.db.execute_query(query_insertar, params)

            # Insertar en 'historicoLibros'
            self.db.execute_query(query_insertar_historico, params_historico)

            # Insertar ejemplares en la tabla 'ejemplares' para el libro registrado
            for _ in range(cantidad_disponible):
                query_insertar_ejemplar = """
                INSERT INTO ejemplares (libro_isbn, estado)
                VALUES (?, 'en condiciones')
                """
                self.db.execute_query(query_insertar_ejemplar, (isbn,))
            
            # Confirmar los cambios
            self.db.commit()
            print(f"Libro '{titulo}' registrado con éxito, junto con {cantidad_disponible} ejemplares.")
            return "Éxito"
        except IntegrityError as e:
            print(f"Error al registrar el libro: {e}")
            return "Error de integridad"


        
    def buscar_libros(self, criterio):
        # Buscar libros junto con el nombre y apellido del autor
        query = """
        SELECT 
            libros.isbn, 
            libros.titulo, 
            libros.genero, 
            libros.anio_publicacion, 
            autores.nombre || ' ' || autores.apellido AS autor_nombre, 
            libros.cantidad_disponible 
        FROM libros
        JOIN autores ON libros.autor_id = autores.id
        WHERE libros.isbn = ? OR libros.titulo LIKE ?
        """
        params = (criterio, f"%{criterio}%")
        resultados = self.db.fetch_query(query, params)
        return resultados
    def eliminar_libro(self, isbn):
        # Eliminar ejemplares asociados
        query_eliminar_ejemplares = "DELETE FROM ejemplares WHERE libro_isbn = ?"
        self.db.execute_query(query_eliminar_ejemplares, (isbn,))
        
        # Eliminar el libro de la tabla 'libros'
        query_eliminar_libro = "DELETE FROM libros WHERE isbn = ?"
        try:
            self.db.execute_query(query_eliminar_libro, (isbn,))
            self.db.commit()
            return "Éxito"
        except Exception as e:
            print(f"Error al eliminar libro: {e}")
            return f"Error: {e}"



