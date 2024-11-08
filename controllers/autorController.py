from database.conexionBDA import DbSingleton
from models.autor import Autor

class AutorController:
    def __init__(self):
        self.db = DbSingleton()

    def registrar_autor(self, nombre, apellido, nacionalidad):
        query = """
        INSERT INTO autores (nombre, apellido, nacionalidad)
        VALUES (?, ?, ?)
        """
        params = (nombre, apellido, nacionalidad)
        self.db.execute_query(query, params)
        self.db.commit()
        print(f"Autor {nombre} {apellido} registrado con éxito")
