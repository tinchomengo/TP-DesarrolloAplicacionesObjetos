import sqlite3
from sqlite3 import Error
import os

class DbSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DbSingleton, cls).__new__(cls)
            try:
                cls._instance._initialize_connection()
            except Error as e:
                print(f"Error al conectar a SQLite: {e}")
                cls._instance = None
        return cls._instance

    def _initialize_connection(self):
        try:
            # Ruta relativa a la base de datos
            db_path = os.path.join(os.path.dirname(__file__), "biblioteca.db")
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            print("Conexión con la base de datos establecida")
        except Error as e:
            print(f"Error al conectarse: {e}")
            self.connection = None  # Asegura que la conexión sea None si falla

    def execute_query(self, query, params=()):
        try:
            self.test_connection()
            self.cursor.execute(query, params)
        except Error as e:
            print(f"Error al intentar ejecutar la consulta: {e}")
            raise e

    def fetch_query(self, query, parameters=()):
        try:
            self.test_connection()
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al intentar obtener datos: {e}")
            raise e

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Conexión a la base de datos cerrada")

    def test_connection(self):
        if not self.connection:
            self._initialize_connection()

    def commit(self):
        if self.connection:
            self.connection.commit()
            print("Cambios guardados en la base de datos")


if __name__ == "__main__":
    db = DbSingleton()
    db.execute_query("SELECT sqlite_version();")  # Verifica la conexión
    db.close_connection()
