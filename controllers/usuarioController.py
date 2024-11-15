from database.conexionBDA import DbSingleton
from models.usuario import Usuario

class UsuarioController:
    def __init__(self):
        self.db = DbSingleton()

    def registrar_usuario(self, nombre, apellido, tipo_usuario, direccion, telefono):
        query = """
        INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (nombre, apellido, tipo_usuario, direccion, telefono)
        self.db.execute_query(query, params)
        self.db.commit()
        print(f"Usuario {nombre} {apellido} registrado con éxito")
    def buscar_usuarios_por_nombre(self, nombre):
        query = """
        SELECT * FROM usuarios
        WHERE nombre LIKE ? OR apellido LIKE ?
        """
        params = (f"%{nombre}%", f"%{nombre}%")
        resultados = self.db.fetch_query(query, params)
        return resultados

