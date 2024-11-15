from conexionBDA import DbSingleton

def crear_tablas():
    db = DbSingleton()

    # Tabla de Autores
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS autores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            nacionalidad TEXT
        )
    """)

    # Tabla de Libros
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS libros (
            isbn TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            genero TEXT,
            anio_publicacion INTEGER,
            autor_id INTEGER,
            cantidad_disponible INTEGER NOT NULL,
            FOREIGN KEY (autor_id) REFERENCES autores(id)
        )
    """)

    # Tabla de Usuarios
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            tipo_usuario TEXT CHECK(tipo_usuario IN ('estudiante', 'profesor')),
            direccion TEXT,
            telefono TEXT,
            multa INTEGER DEFAULT 0
        )
    """)

    # Tabla de Ejemplares
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS ejemplares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_isbn TEXT NOT NULL,
            estado TEXT DEFAULT 'en condiciones',
            FOREIGN KEY (libro_isbn) REFERENCES libros(isbn)
        )
    """)
    
    # Tabla de Préstamos con las nuevas columnas para fechas de devolución estimada y real
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            ejemplar_id INTEGER,
            fecha_prestamo DATE NOT NULL,
            fecha_devolucion_estimada DATE,  -- Nueva columna para la fecha de devolución estimada
            fecha_devolucion_real DATE,      -- Nueva columna para la fecha de devolución real
            estado TEXT DEFAULT 'en condiciones',
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (ejemplar_id) REFERENCES ejemplares(id)
        )
    """)

    db.commit()
    print("Tablas Creadas")
def crear_tabla_individual():
    db = DbSingleton()

    db.execute_query("""
            CREATE TABLE historicoLibros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            anio_publicacion INTEGER NOT NULL,
            autor_id INTEGER NOT NULL,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)


if __name__ == "__main__":
    crear_tablas()
