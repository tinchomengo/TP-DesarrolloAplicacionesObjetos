from conexionBDA import DbSingleton

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
        ("Carlos", "Pérez", "estudiante", "Calle Falsa 123", "555-1234"),
        ("Ana", "Gómez", "profesor", "Avenida Siempre Viva 456", "555-5678"),
        ("Luis", "Martínez", "estudiante", "Boulevard de los Sueños 789", "555-8765"),
        ("María", "López", "profesor", "Camino del Rey 101", "555-4321"),
        ("José", "Rodríguez", "estudiante", "Vía Láctea 202", "555-3456")
    ]
    for nombre, apellido, tipo_usuario, direccion, telefono in usuarios:
        db.execute_query("""
            INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, apellido, tipo_usuario, direccion, telefono))

    # Insertar ejemplares para cada libro según la cantidad disponible
    for isbn, _, _, _, _, cantidad_disponible in libros:
        for _ in range(cantidad_disponible):
            db.execute_query("""
                INSERT INTO ejemplares (libro_isbn, estado)
                VALUES (?, 'en condiciones')
            """, (isbn,))

    db.commit()
    print("Datos insertados correctamente")

if __name__ == "__main__":
    insertar_datos()
