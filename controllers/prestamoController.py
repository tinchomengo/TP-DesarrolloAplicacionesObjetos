from database.conexionBDA import DbSingleton
from datetime import datetime, timedelta

class PrestamoController:
    def __init__(self):
        self.db = DbSingleton()

    # Reporte 1: Listar todos los préstamos vencidos
    def listar_prestamos_vencidos(self):
        # Obtener préstamos vencidos donde la fecha de devolución real es mayor a la estimada
        query = """
        SELECT 
            prestamos.id,
            usuarios.nombre || ' ' || usuarios.apellido AS usuario, 
            libros.titulo AS libro, 
            prestamos.fecha_devolucion_estimada, 
            prestamos.fecha_devolucion_real,
            JULIANDAY(prestamos.fecha_devolucion_real) - JULIANDAY(prestamos.fecha_devolucion_estimada) AS dias_atraso
        FROM prestamos
        JOIN usuarios ON prestamos.usuario_id = usuarios.id
        JOIN ejemplares ON prestamos.ejemplar_id = ejemplares.id
        JOIN libros ON ejemplares.libro_isbn = libros.isbn
        WHERE prestamos.fecha_devolucion_real > prestamos.fecha_devolucion_estimada
        """
        resultado = self.db.fetch_query(query)
        return resultado


    # Reporte 2: Listar los libros más prestados en el último mes
    def libros_mas_prestados_ultimo_mes(self):
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

    def registrar_prestamo(self, usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion_estimada):
        # Convert dates to datetime objects for comparison
        fecha_prestamo_dt = datetime.strptime(fecha_prestamo, "%Y-%m-%d")
        fecha_devolucion_estimada_dt = datetime.strptime(fecha_devolucion_estimada, "%Y-%m-%d")

        # Validate that the estimated return date is after the loan date
        if fecha_devolucion_estimada_dt <= fecha_prestamo_dt:
            print("La fecha de devolución estimada debe ser posterior a la fecha de préstamo.")
            return "La fecha de devolución estimada debe ser posterior a la fecha de préstamo."

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

        # Registrar el préstamo con fecha_devolucion_estimada
        prestamo_query = """
        INSERT INTO prestamos (usuario_id, ejemplar_id, fecha_prestamo, fecha_devolucion_estimada)
        VALUES (?, ?, ?, ?)
        """
        prestamo_params = (usuario_id, ejemplar_id, fecha_prestamo, fecha_devolucion_estimada)
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

    def registrar_devolucion(self, prestamo_id, estado, fecha_devolucion_real):
        # Obtener información del préstamo
        query_prestamo = "SELECT usuario_id, fecha_devolucion_estimada FROM prestamos WHERE id = ?"
        prestamo = self.db.fetch_query(query_prestamo, (prestamo_id,))
        if not prestamo:
            return "Préstamo no encontrado."

        usuario_id, fecha_devolucion_estimada = prestamo[0]

        # Get the related copy (ejemplar) ID
        ejemplar_query = "SELECT ejemplar_id FROM prestamos WHERE id = ?"
        ejemplar_id = self.db.fetch_query(ejemplar_query, (prestamo_id,))[0][0]

        # Update the state of the copy based on the returned condition (in good condition or damaged)
        actualizar_ejemplar_estado_query = "UPDATE ejemplares SET estado = ? WHERE id = ?"
        self.db.execute_query(actualizar_ejemplar_estado_query, (estado, ejemplar_id))

        # Incrementar la cantidad disponible del libro en la tabla `libros`
        if estado == "en condiciones":
            actualizar_cantidad_libro_query = """
            UPDATE libros 
            SET cantidad_disponible = cantidad_disponible + 1 
            WHERE isbn = (SELECT libro_isbn FROM ejemplares WHERE id = ?)
            """
            self.db.execute_query(actualizar_cantidad_libro_query, (ejemplar_id,))

        # Calcular días de retraso
        fecha_devolucion_estimada = datetime.strptime(fecha_devolucion_estimada, "%Y-%m-%d")
        fecha_devolucion_real = datetime.strptime(fecha_devolucion_real, "%Y-%m-%d")
        dias_retraso = (fecha_devolucion_real - fecha_devolucion_estimada).days

        multa = 0
        if dias_retraso > 0:
            multa = dias_retraso * 100

            # Actualizar la multa del usuario
            query_actualizar_multa = "UPDATE usuarios SET multa = multa + ? WHERE id = ?"
            self.db.execute_query(query_actualizar_multa, (multa, usuario_id))

        # Actualizar el estado del préstamo
        query_actualizar_prestamo = """
        UPDATE prestamos
        SET estado = ?, fecha_devolucion_real = ?
        WHERE id = ?
        """
        self.db.execute_query(query_actualizar_prestamo, (estado, fecha_devolucion_real, prestamo_id))
        self.db.commit()

        return "Éxito"

    def obtener_prestamos_activos(self):
        query = """
        SELECT prestamos.id, 
            usuarios.nombre || ' ' || usuarios.apellido AS usuario,
            libros.titulo AS libro, 
            prestamos.fecha_prestamo, 
            prestamos.fecha_devolucion_estimada
        FROM prestamos
        INNER JOIN usuarios ON prestamos.usuario_id = usuarios.id
        INNER JOIN ejemplares ON prestamos.ejemplar_id = ejemplares.id
        INNER JOIN libros ON ejemplares.libro_isbn = libros.isbn
        WHERE prestamos.fecha_devolucion_real IS NULL
        """
        resultados = self.db.fetch_query(query)
        print(f"Resultados de la consulta: {resultados}")
        return resultados
    def obtener_todos_los_prestamos(self):
        query = """
        SELECT prestamos.id, 
            usuarios.nombre || ' ' || usuarios.apellido AS usuario,
            libros.titulo AS libro, 
            prestamos.fecha_prestamo, 
            prestamos.fecha_devolucion_estimada,
            COALESCE(prestamos.fecha_devolucion_real, 'Pendiente') AS fecha_devolucion_real
        FROM prestamos
        JOIN usuarios ON prestamos.usuario_id = usuarios.id
        JOIN ejemplares ON prestamos.ejemplar_id = ejemplares.id
        JOIN libros ON ejemplares.libro_isbn = libros.isbn
        """
        resultados = self.db.fetch_query(query)
        print(f"Préstamos obtenidos: {resultados}")
        return resultados
    def obtener_total_prestamos(self):
        query = "SELECT COUNT(*) FROM prestamos"
        total = self.db.fetch_query(query)
        return total[0][0] if total else 0
    
    def eliminar_prestamo(self, prestamo_id):
        try:
            query = "DELETE FROM prestamos WHERE id = ?"
            self.db.execute_query(query, (prestamo_id,))
            self.db.commit()
            print(f"Préstamo ID {prestamo_id} eliminado exitosamente.")
            return "Éxito"
        except Exception as e:
            print(f"Error al eliminar el préstamo ID {prestamo_id}: {e}")
            return "Error"



