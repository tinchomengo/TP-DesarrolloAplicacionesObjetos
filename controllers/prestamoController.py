from database.conexionBDA import DbSingleton
from datetime import datetime, timedelta

class PrestamoController:
    def __init__(self):
        self.db = DbSingleton()

        # Reporte 1: Listar todos los préstamos vencidos
    def listar_prestamos_vencidos(self):
        # Asumimos que prestamos vencidos son aquellos donde la fecha de devolución estimada ha pasado y aún no han sido devueltos
        query = """
        SELECT prestamos.id, usuarios.nombre || ' ' || usuarios.apellido AS usuario,
               libros.titulo AS libro, prestamos.fecha_prestamo, prestamos.fecha_devolucion
        FROM prestamos
        JOIN usuarios ON prestamos.usuario_id = usuarios.id
        JOIN ejemplares ON prestamos.ejemplar_id = ejemplares.id
        JOIN libros ON ejemplares.libro_isbn = libros.isbn
        WHERE prestamos.fecha_devolucion IS NULL
          AND prestamos.fecha_prestamo < DATE('now', '-30 days')
        """
        resultado = self.db.fetch_query(query)
        return resultado

    # Reporte 2: Listar los libros más prestados en el último mes
    def libros_mas_prestados_ultimo_mes(self):
        # Asumimos que un préstamo cuenta dentro del mes si su fecha de préstamo es dentro de los últimos 30 días
        fecha_hace_un_mes = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        query = """
        SELECT libros.titulo, COUNT(prestamos.id) AS total_prestamos
        FROM prestamos
        JOIN ejemplares ON prestamos.ejemplar_id = ejemplares.id
        JOIN libros ON ejemplares.libro_isbn = libros.isbn
        WHERE prestamos.fecha_prestamo >= ?
        GROUP BY libros.titulo
        ORDER BY total_prestamos DESC
        """
        resultado = self.db.fetch_query(query, (fecha_hace_un_mes,))
        return resultado

    # Reporte 3: Listar los usuarios que han tomado más libros en préstamo
    def usuarios_mas_prestamos(self):
        query = """
        SELECT usuarios.nombre || ' ' || usuarios.apellido AS usuario, COUNT(prestamos.id) AS total_prestamos
        FROM prestamos
        JOIN usuarios ON prestamos.usuario_id = usuarios.id
        GROUP BY usuarios.id
        ORDER BY total_prestamos DESC
        """
        resultado = self.db.fetch_query(query)
        return resultado

    def registrar_prestamo(self, usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion):
        # Obtener el tipo de usuario (estudiante o profesor)
        tipo_usuario_query = "SELECT tipo_usuario FROM usuarios WHERE id = ?"
        resultado_usuario = self.db.fetch_query(tipo_usuario_query, (usuario_id,))
        if not resultado_usuario:
            print("El ID de usuario no existe.")
            return "Usuario no encontrado"
        
        tipo_usuario = resultado_usuario[0][0]
        
        # Contar préstamos activos del usuario
        prestamos_activos_query = """
        SELECT COUNT(*) FROM prestamos 
        WHERE usuario_id = ?
        """
        prestamos_activos = self.db.fetch_query(prestamos_activos_query, (usuario_id,))[0][0]

        print(f"Prestamos activos: {prestamos_activos}")
        
        # Verificar límite de préstamos
        limite_prestamos = 3 if tipo_usuario == "estudiante" else 5
        if prestamos_activos >= limite_prestamos:
            print(f"El usuario {tipo_usuario} ha alcanzado el límite de préstamos.")
            return "Límite de préstamos alcanzado"

        # Verificar disponibilidad de ejemplares del libro
        ejemplar_query = """
        SELECT id FROM ejemplares
        WHERE libro_isbn = ? AND estado = 'en condiciones'
        LIMIT 1
        """
        ejemplar_result = self.db.fetch_query(ejemplar_query, (libro_isbn,))
        if not ejemplar_result:
            print("No hay ejemplares disponibles para este libro.")
            return "No hay ejemplares disponibles"

        ejemplar_id = ejemplar_result[0][0]

        # Registrar el préstamo
        prestamo_query = """
        INSERT INTO prestamos (usuario_id, ejemplar_id, fecha_prestamo, fecha_devolucion)
        VALUES (?, ?, ?, ?)
        """
        prestamo_params = (usuario_id, ejemplar_id, fecha_prestamo, fecha_devolucion)
        self.db.execute_query(prestamo_query, prestamo_params)

        # Actualizar estado del ejemplar a "prestado"
        actualizar_ejemplar_query = "UPDATE ejemplares SET estado = 'prestado' WHERE id = ?"
        self.db.execute_query(actualizar_ejemplar_query, (ejemplar_id,))

        # Disminuir la cantidad disponible del libro en 1
        actualizar_cantidad_libro_query = """
        UPDATE libros 
        SET cantidad_disponible = cantidad_disponible - 1 
        WHERE isbn = ?
        """
        self.db.execute_query(actualizar_cantidad_libro_query, (libro_isbn,))

        # Confirmar cambios
        self.db.commit()
        print(f"Préstamo registrado para el libro ISBN {libro_isbn} con ejemplar ID {ejemplar_id} para el usuario ID {usuario_id}")
        return "Éxito"

    def registrar_devolucion(self, prestamo_id, estado):
        # Registrar la devolución del préstamo
        devolver_prestamo_query = """
        UPDATE prestamos 
        SET fecha_devolucion = CURRENT_DATE
        WHERE id = ? AND fecha_devolucion IS NULL
        """
        self.db.execute_query(devolver_prestamo_query, (prestamo_id,))

        # Obtener el ejemplar asociado al préstamo
        ejemplar_query = "SELECT ejemplar_id FROM prestamos WHERE id = ?"
        ejemplar_id = self.db.fetch_query(ejemplar_query, (prestamo_id,))[0][0]

        # Actualizar el estado del ejemplar según la devolución (en condiciones o dañado)
        actualizar_ejemplar_estado_query = "UPDATE ejemplares SET estado = ? WHERE id = ?"
        self.db.execute_query(actualizar_ejemplar_estado_query, (estado, ejemplar_id))

        # Incrementar la cantidad disponible del libro en la tabla `libros`
        actualizar_cantidad_libro_query = """
        UPDATE libros 
        SET cantidad_disponible = cantidad_disponible + 1 
        WHERE isbn = (SELECT libro_isbn FROM ejemplares WHERE id = ?)
        """
        self.db.execute_query(actualizar_cantidad_libro_query, (ejemplar_id,))

        # Confirmar cambios
        self.db.commit()
        print(f"Devolución registrada para el préstamo ID {prestamo_id}")
        return "Éxito"
