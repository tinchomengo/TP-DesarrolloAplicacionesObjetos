from conexionBDA import DbSingleton

def limpiar_base_de_datos():
    db = DbSingleton()
    
    # Eliminación de todos los datos de cada tabla
    tablas = ["prestamos", "usuarios", "libros", "autores", "ejemplares"]
    for tabla in tablas:
        print("Limpiando...")
        db.execute_query(f"DELETE FROM {tabla}")
        db.execute_query(f"DELETE FROM sqlite_sequence WHERE name='{tabla}';")  # Reinicia IDs autoincrementales
    db.commit()
    print("Base de datos limpiada con éxito")

def borrar_tabla(tabla):
    db = DbSingleton()
    db.execute_query(f"DELETE FROM {tabla}")
    db.execute_query(f"DELETE FROM sqlite_sequence WHERE name='{tabla}';")  # Reinicia IDs autoincrementales
    db.commit()
    print(f"Tabla {tabla} limpiada con éxito")

def borrar_todas_las_tablas():
    db = DbSingleton()
    tablas = ["prestamos", "usuarios", "libros", "autores", "ejemplares"]
    for tabla in tablas:
        borrar_tabla(tabla)
    print("Todas las tablas limpiadas con éxito")

if __name__ == "__main__":
    limpiar_base_de_datos()
