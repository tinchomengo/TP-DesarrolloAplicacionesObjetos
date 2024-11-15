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
    def eliminar_usuario(self, usuario_id):
        """
        Elimina un usuario de la base de datos por su ID.
        :param usuario_id: ID del usuario a eliminar
        :return: 'Éxito' si se eliminó correctamente, de lo contrario lanza una excepción.
        """
        try:
            # Verificar si el usuario tiene préstamos activos
            query_verificar_prestamos = """
            SELECT COUNT(*) FROM prestamos WHERE usuario_id = ? AND fecha_devolucion_real IS NULL
            """
            prestamos_activos = self.db.fetch_query(query_verificar_prestamos, (usuario_id,))[0][0]

            if prestamos_activos > 0:
                return "El usuario tiene préstamos activos. No se puede eliminar."

            # Eliminar al usuario
            query_eliminar = "DELETE FROM usuarios WHERE id = ?"
            self.db.execute_query(query_eliminar, (usuario_id,))
            self.db.commit()
            print(f"Usuario con ID {usuario_id} eliminado exitosamente.")
            return "Éxito"
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            raise Exception("Error al intentar eliminar el usuario.")

