from conexionBDA import DbSingleton

def prueba_conexion_y_consulta():
    db = DbSingleton()

    # Inserta un autor para probar
    db.execute_query("""
        INSERT INTO autores (nombre, apellido, nacionalidad)
        VALUES (?, ?, ?)
    """, ("Gabriel", "García Márquez", "Colombiano"))

    # Recupera el autor que acabas de insertar
    autores = db.fetch_query("SELECT * FROM autores")
    print("Autores en la base de datos:")
    for autor in autores:
        print(autor)

    db.close_connection()

if __name__ == "__main__":
    prueba_conexion_y_consulta()
