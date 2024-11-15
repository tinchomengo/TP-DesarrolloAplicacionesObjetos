from database.conexionBDA import DbSingleton
from models.libro import Libro
from sqlite3 import IntegrityError

class LibroController:
    def __init__(self):
        self.db = DbSingleton()

    def registrar_libro(self, isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible):
        # Verificar si el ISBN ya existe
        query_verificar = "SELECT * FROM libros WHERE isbn = ?"
        if self.db.fetch_query(query_verificar, (isbn,)):
            print(f"El ISBN {isbn} ya existe en la base de datos.")
            return "ISBN duplicado"
        
        # Insertar el libro si el ISBN no está duplicado
        query_insertar = """
        INSERT INTO libros (isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)
        try:
            self.db.execute_query(query_insertar, params)

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

