from conexionBDA import DbSingleton
from datetime import datetime, timedelta

def insertar_datos():
    db = DbSingleton()

    # Insertar autores
    autores = [
        ("Gabriel", "García Márquez", "Colombiano"),
        ("Jorge Luis", "Borges", "Argentino"),
        ("Jane", "Austen", "Británica"),
        ("Fyodor", "Dostoevsky", "Ruso"),
        ("Haruki", "Murakami", "Japonés")
    ]
    for nombre, apellido, nacionalidad in autores:
        db.execute_query("""
            INSERT INTO autores (nombre, apellido, nacionalidad)
            VALUES (?, ?, ?)
        """, (nombre, apellido, nacionalidad))

    # Insertar libros
    libros = [
        ("978-3-16-148410-0", "Cien Años de Soledad", "Novela", 1967, 1, 10),
        ("978-3-16-148410-1", "El Aleph", "Ficción", 1949, 2, 8),
        ("978-3-16-148410-2", "Orgullo y Prejuicio", "Romance", 1813, 3, 7),
        ("978-3-16-148410-3", "Crimen y Castigo", "Filosofía", 1866, 4, 5),
        ("978-3-16-148410-4", "Tokio Blues", "Drama", 1987, 5, 9)
    ]
    for isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible in libros:
        db.execute_query("""
            INSERT INTO libros (isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (isbn, titulo, genero, anio_publicacion, autor_id, cantidad_disponible))

    # Insertar usuarios
    usuarios = [
        ("Carlos", "Pérez", "estudiante", "Calle Falsa 123", "555-1234", 0),
        ("Ana", "Gómez", "profesor", "Avenida Siempre Viva 456", "555-5678", 0),
        ("Luis", "Martínez", "estudiante", "Boulevard de los Sueños 789", "555-8765", 0),
        ("María", "López", "profesor", "Camino del Rey 101", "555-4321", 0),
        ("José", "Rodríguez", "estudiante", "Vía Láctea 202", "555-3456", 0)
    ]
    for nombre, apellido, tipo_usuario, direccion, telefono, multa in usuarios:
        db.execute_query("""
            INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono, multa)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, tipo_usuario, direccion, telefono, multa))

    # Insertar ejemplares para cada libro según la cantidad disponible
    for isbn, _, _, _, _, cantidad_disponible in libros:
        for _ in range(cantidad_disponible):
            db.execute_query("""
                INSERT INTO ejemplares (libro_isbn, estado)
                VALUES (?, 'en condiciones')
            """, (isbn,))

    # Insertar préstamos con fechas de préstamo y devolución estimada
    prestamos = [
        (1, 1, datetime.now().strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"), None),
        (2, 2, datetime.now().strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"), None),
        (3, 3, datetime.now().strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), None),
        (4, 4, datetime.now().strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d"), None),
        (5, 5, datetime.now().strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"), None)
    ]
    for usuario_id, ejemplar_id, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real in prestamos:
        db.execute_query("""
            INSERT INTO prestamos (usuario_id, ejemplar_id, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real)
            VALUES (?, ?, ?, ?, ?)
        """, (usuario_id, ejemplar_id, fecha_prestamo, fecha_devolucion_estimada, fecha_devolucion_real))

    db.commit()
    print("Datos insertados correctamente")

if __name__ == "__main__":
    insertar_datos()
