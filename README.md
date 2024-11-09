# Desarrollo de Aplicaciones con Objetos - UTN FRC (2024)

**Trabajo Práctico Integrador**

**Integrantes:**

- Imoberdorf, Martín
- Mengo, Martín
- Pontelli, Matteo
- Rodriguez, Isauro Manuel

## Ejercicio 1: Sistema de Gestión de Biblioteca

### Objetivo

Desarrollar un sistema de gestión para una biblioteca que permita manejar libros, autores, préstamos y devoluciones. El sistema deberá cumplir con los requisitos de clases y operaciones detallados a continuación, incluyendo validaciones y reportes.

### Requerimientos

#### Clases

- **Libro**: contiene información del código ISBN, título, género, año de publicación, autor, y cantidad disponible.
- **Autor**: representa a cada autor con su ID, nombre, apellido y nacionalidad.
- **Usuario**: contiene el ID, nombre, apellido, tipo de usuario (estudiante o profesor), dirección y teléfono.
- **Préstamo**: registro de préstamo de un libro con ID, usuario, libro, fecha de préstamo y fecha de devolución.

#### Operaciones

1. **Registro de Autores**: permite el registro de nuevos autores en el sistema.
2. **Registro de Libros**: permite el registro de nuevos libros y asignarlos a un autor.
3. **Registro de Usuarios**: permite el registro de nuevos usuarios.
4. **Préstamo de Libros**: asigna un libro a un usuario con la fecha de préstamo y una fecha de devolución estimada.
5. **Devolución de Libros**: permite registrar la devolución de un libro y verificar su estado al momento de la devolución.
6. **Consulta de Disponibilidad**: consulta la disponibilidad de un libro.
7. **Reportes**:
   - Listar todos los préstamos vencidos.
   - Generar un listado de los libros más prestados durante el último mes.
   - Reportar los usuarios que han tomado más libros en préstamo.

### Dificultad Extra

- **Validaciones**:
  - Verificar que no se puedan prestar libros que no están disponibles.
  - No permitir prestar más de 3 libros a estudiantes y más de 5 a profesores.
- **Tipos de Reportes**:
  - Generar reportes en formato tabular y gráfico (por ejemplo, un gráfico de barras mostrando los géneros más populares).

### Operaciones Adicionales (Opcionales)

1. **Reserva de Libros**: permite a los usuarios reservar libros no disponibles y notificarlos cuando estén disponibles.
2. **Penalización por Retrasos**: sistema de penalización para usuarios que devuelven libros con retraso, calculando automáticamente el monto de la multa.
3. **Registro de Donaciones**: permite registrar donaciones de libros de usuarios o instituciones, incorporando estos libros al inventario.
4. **Baja de Libros**: funcionalidad para dar de baja a libros dañados o perdidos, manteniendo un registro histórico.

### Reportes Adicionales

- **Reporte de Libros por Autor**: listado de todos los libros por autor, incluyendo la cantidad disponible por cada uno.
- **Reporte de Usuarios con Penalizaciones**: lista de usuarios con penalizaciones activas, detallando el monto de la penalización y el motivo.
- **Estadísticas de Donaciones**: reporte de las donaciones recibidas en un periodo determinado, con un gráfico de libros donados por mes.

---

Este sistema de gestión bibliotecaria está diseñado para ser flexible, eficiente y fácil de usar, proporcionando a los administradores de la biblioteca herramientas clave para mantener el control sobre los préstamos, el inventario y las estadísticas de uso.
