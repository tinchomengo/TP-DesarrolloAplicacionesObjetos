import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Inicializamos el controlador de préstamo

from controllers.autorController import AutorController
from controllers.libroController import LibroController
from controllers.usuarioController import UsuarioController
from controllers.prestamoController import PrestamoController

# Inicializamos los controladores
autor_controller = AutorController()
libro_controller = LibroController()
usuario_controller = UsuarioController()
prestamo_controller = PrestamoController()

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.geometry("800x600")
        title_label = tk.Label(
            self.root,
            text="Menú de Opciones",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(side=tk.TOP, pady=(20, 10))  # Ajusta el padding para dar espacio

        # Crear botones en columna
        self.create_buttons()
    
    def create_buttons(self):
        # Crear un marco lateral para los botones
        button_frame = tk.Frame(self.root)

        button_frame.pack(side=tk.TOP, fill=tk.Y, padx=10, pady=10)

        # Configuración de los botones
        buttons = [
            ("Registro de Autores", self.open_autores_window),
            ("Registro de Libros", self.open_libros_window),
            ("Registro de Usuarios", self.open_usuarios_window),
            ("Préstamo de Libros", self.open_prestamo_window),
            ("Devolución de Libros", self.open_devolucion_window),
            ("Consulta de Disponibilidad", self.open_consulta_disponibilidad_window),
            ("Reportes", self.open_reportes_window)
        ]

        for text, command in buttons:
            button = tk.Button(button_frame, text=text, command=command, width=20, height=3)
            button.pack(pady=5)

    def open_autores_window(self):
        # Ventana para registrar autores
        autores_window = tk.Toplevel(self.root)
        autores_window.title("Registro de Autores")
        autores_window.geometry("400x300")
        
        tk.Label(autores_window, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        nombre_autor = tk.Entry(autores_window)
        nombre_autor.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(autores_window, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        apellido_autor = tk.Entry(autores_window)
        apellido_autor.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(autores_window, text="Nacionalidad:").grid(row=2, column=0, padx=5, pady=5)
        nacionalidad_autor = tk.Entry(autores_window)
        nacionalidad_autor.grid(row=2, column=1, padx=5, pady=5)
        
        def registrar_autor():
            nombre = nombre_autor.get()
            apellido = apellido_autor.get()
            nacionalidad = nacionalidad_autor.get()
            
            if nombre and apellido and nacionalidad:
                autor_controller.registrar_autor(nombre, apellido, nacionalidad)
                messagebox.showinfo("Éxito", "Autor registrado exitosamente", parent=autores_window)
                nombre_autor.delete(0, tk.END)
                apellido_autor.delete(0, tk.END)
                nacionalidad_autor.delete(0, tk.END)
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios", parent=autores_window)
        
        tk.Button(autores_window, text="Registrar Autor", command=registrar_autor).grid(row=3, columnspan=2, pady=10)

    def open_libros_window(self):
        # Ventana para registrar libros
        libros_window = tk.Toplevel(self.root)
        libros_window.title("Registro de Libros")
        libros_window.geometry("400x400")
        
        tk.Label(libros_window, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
        isbn_libro = tk.Entry(libros_window)
        isbn_libro.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(libros_window, text="Título:").grid(row=1, column=0, padx=5, pady=5)
        titulo_libro = tk.Entry(libros_window)
        titulo_libro.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(libros_window, text="Género:").grid(row=2, column=0, padx=5, pady=5)
        genero_libro = tk.Entry(libros_window)
        genero_libro.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(libros_window, text="Año de Publicación:").grid(row=3, column=0, padx=5, pady=5)
        anio_libro = tk.Entry(libros_window)
        anio_libro.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(libros_window, text="Cantidad Disponible:").grid(row=4, column=0, padx=5, pady=5)
        cantidad_libro = tk.Entry(libros_window)
        cantidad_libro.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(libros_window, text="ID del Autor:").grid(row=5, column=0, padx=5, pady=5)
        autor_id_libro = tk.Entry(libros_window)
        autor_id_libro.grid(row=5, column=1, padx=5, pady=5)
        
        def registrar_libro():
            isbn = isbn_libro.get()
            titulo = titulo_libro.get()
            genero = genero_libro.get()
            anio = anio_libro.get()
            cantidad = cantidad_libro.get()
            autor_id = autor_id_libro.get()
            
            if isbn and titulo and genero and anio.isdigit() and cantidad.isdigit() and autor_id.isdigit():
                resultado = libro_controller.registrar_libro(
                    isbn=isbn,
                    titulo=titulo,
                    genero=genero,
                    anio_publicacion=int(anio),
                    autor_id=int(autor_id),
                    cantidad_disponible=int(cantidad)
                )

                if resultado == "Éxito":
                    messagebox.showinfo("Éxito", "Libro registrado exitosamente", parent=libros_window)
                    isbn_libro.delete(0, tk.END)
                    titulo_libro.delete(0, tk.END)
                    genero_libro.delete(0, tk.END)
                    anio_libro.delete(0, tk.END)
                    cantidad_libro.delete(0, tk.END)
                    autor_id_libro.delete(0, tk.END)
                elif resultado == "ISBN duplicado":
                    messagebox.showwarning("Advertencia", "El ISBN ya existe en la base de datos.", parent=libros_window)
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios y deben ser numéricos donde corresponda", parent=libros_window)

        tk.Button(libros_window, text="Registrar Libro", command=registrar_libro).grid(row=6, columnspan=2, pady=10)

    def open_usuarios_window(self):
        # Ventana para registrar usuarios
        usuarios_window = tk.Toplevel(self.root)
        usuarios_window.title("Registro de Usuarios")
        usuarios_window.geometry("400x300")
        
        tk.Label(usuarios_window, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        nombre_usuario = tk.Entry(usuarios_window)
        nombre_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(usuarios_window, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        apellido_usuario = tk.Entry(usuarios_window)
        apellido_usuario.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(usuarios_window, text="Tipo de Usuario:").grid(row=2, column=0, padx=5, pady=5)
        tipo_usuario = ttk.Combobox(usuarios_window, values=["estudiante", "profesor"])
        tipo_usuario.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(usuarios_window, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
        direccion_usuario = tk.Entry(usuarios_window)
        direccion_usuario.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(usuarios_window, text="Teléfono:").grid(row=4, column=0, padx=5, pady=5)
        telefono_usuario = tk.Entry(usuarios_window)
        telefono_usuario.grid(row=4, column=1, padx=5, pady=5)

        def registrar_usuario():
            nombre = nombre_usuario.get()
            apellido = apellido_usuario.get()
            tipo = tipo_usuario.get()
            direccion = direccion_usuario.get()
            telefono = telefono_usuario.get()

            if nombre and apellido and tipo and direccion and telefono:
                usuario_controller.registrar_usuario(nombre, apellido, tipo, direccion, telefono)
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente", parent=usuarios_window)
                nombre_usuario.delete(0, tk.END)
                apellido_usuario.delete(0, tk.END)
                tipo_usuario.set("")
                direccion_usuario.delete(0, tk.END)
                telefono_usuario.delete(0, tk.END)
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios", parent=usuarios_window)

        tk.Button(usuarios_window, text="Registrar Usuario", command=registrar_usuario).grid(row=5, columnspan=2, pady=10)
    



    def open_consulta_disponibilidad_window(self):
        # Ventana para consulta de disponibilidad de libros
        consulta_window = tk.Toplevel(self.root)
        consulta_window.title("Consulta de Disponibilidad de Libros")
        consulta_window.geometry("500x400")

        tk.Label(consulta_window, text="Buscar por ISBN o Título:").pack(pady=10)
        criterio_entry = tk.Entry(consulta_window, width=30)
        criterio_entry.pack(pady=5)

        resultado_listbox = tk.Listbox(consulta_window, width=50, height=15)
        resultado_listbox.pack(pady=10)

        def buscar_libros():
            criterio = criterio_entry.get()
            if criterio:
                resultados = libro_controller.buscar_libros(criterio)
                resultado_listbox.delete(0, tk.END)  # Limpiar resultados anteriores

                if resultados:
                    for resultado in resultados:
                        isbn, titulo, cantidad_disponible = resultado
                        resultado_listbox.insert(tk.END, f"ISBN: {isbn}, Título: {titulo}, Disponible: {cantidad_disponible}")
                else:
                    resultado_listbox.insert(tk.END, "No se encontraron libros.")

        tk.Button(consulta_window, text="Buscar", command=buscar_libros).pack(pady=5)
    

    def open_prestamo_window(self):
        # Ventana para registrar un préstamo de libro
        prestamo_window = tk.Toplevel(self.root)
        prestamo_window.title("Registrar Préstamo de Libro")
        prestamo_window.geometry("400x300")

        tk.Label(prestamo_window, text="Usuario ID:").grid(row=0, column=0, padx=5, pady=5)
        usuario_id_entry = tk.Entry(prestamo_window)
        usuario_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(prestamo_window, text="Libro ISBN:").grid(row=1, column=0, padx=5, pady=5)
        libro_isbn_entry = tk.Entry(prestamo_window)
        libro_isbn_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(prestamo_window, text="Fecha de Préstamo (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        fecha_prestamo_entry = tk.Entry(prestamo_window)
        fecha_prestamo_entry.grid(row=2, column=1, padx=5, pady=5)
        fecha_prestamo_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Fecha actual por defecto

        tk.Label(prestamo_window, text="Fecha de Devolución (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        fecha_devolucion_entry = tk.Entry(prestamo_window)
        fecha_devolucion_entry.grid(row=3, column=1, padx=5, pady=5)

        def registrar_prestamo():
            usuario_id = usuario_id_entry.get()
            libro_isbn = libro_isbn_entry.get()
            fecha_prestamo = fecha_prestamo_entry.get()
            fecha_devolucion = fecha_devolucion_entry.get()

            if usuario_id.isdigit() and libro_isbn and self.validar_fecha(fecha_prestamo) and self.validar_fecha(fecha_devolucion):
                resultado = prestamo_controller.registrar_prestamo(int(usuario_id), libro_isbn, fecha_prestamo, fecha_devolucion)

                if resultado == "Éxito":
                    messagebox.showinfo("Éxito", "Préstamo registrado exitosamente", parent=prestamo_window)
                    usuario_id_entry.delete(0, tk.END)
                    libro_isbn_entry.delete(0, tk.END)
                    fecha_prestamo_entry.delete(0, tk.END)
                    fecha_devolucion_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Advertencia", resultado, parent=prestamo_window)  # Show the error message
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios y deben tener el formato correcto", parent=prestamo_window)

        tk.Button(prestamo_window, text="Registrar Préstamo", command=registrar_prestamo).grid(row=4, columnspan=2, pady=10)

    def open_devolucion_window(self):
        # Ventana para registrar una devolución de libro
        devolucion_window = tk.Toplevel(self.root)
        devolucion_window.title("Registrar Devolución de Libro")
        devolucion_window.geometry("400x200")

        tk.Label(devolucion_window, text="Préstamo ID:").pack(pady=10)
        prestamo_id_entry = tk.Entry(devolucion_window)
        prestamo_id_entry.pack(pady=5)

        tk.Label(devolucion_window, text="Estado de Devolución:").pack(pady=10)
        estado_combo = ttk.Combobox(devolucion_window, values=["en condiciones", "dañado"])
        estado_combo.pack(pady=5)
        estado_combo.set("en condiciones")

        def registrar_devolucion():
            prestamo_id = prestamo_id_entry.get()
            estado = estado_combo.get()

            if prestamo_id.isdigit():
                resultado = prestamo_controller.registrar_devolucion(int(prestamo_id), estado)
                if resultado == "Éxito":
                    messagebox.showinfo("Éxito", "Devolución registrada exitosamente", parent=devolucion_window)
                    prestamo_id_entry.delete(0, tk.END)
                    estado_combo.set("en condiciones")
                else:
                    messagebox.showwarning("Advertencia", resultado, parent=devolucion_window)
            else:
                messagebox.showwarning("Advertencia", "El ID del préstamo debe ser un número", parent=devolucion_window)

        tk.Button(devolucion_window, text="Registrar Devolución", command=registrar_devolucion).pack(pady=10)


    def validar_fecha(self, fecha_str):
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def open_reportes_window(self):
        reportes_window = tk.Toplevel(self.root)
        reportes_window.title("Seleccionar Reporte")
        reportes_window.geometry("400x300")

        tk.Button(reportes_window, text="Préstamos Vencidos", command=self.mostrar_prestamos_vencidos, width=30).pack(pady=10)
        tk.Button(reportes_window, text="Libros Más Prestados Último Mes", command=self.mostrar_libros_mas_prestados, width=30).pack(pady=10)
        tk.Button(reportes_window, text="Usuarios con Más Préstamos", command=self.mostrar_usuarios_mas_prestamos, width=30).pack(pady=10)

    def generar_pdf(self, titulo, encabezados, filas, nombre_archivo):
        # Obtener la ruta a la carpeta 'reports' en el directorio raíz
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        
        # Crear la carpeta 'reports' si no existe
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Ruta completa del archivo PDF
        pdf_path = os.path.join(reports_dir, nombre_archivo)
        
        # Crear el documento PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        
        # Estilos de documento
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title_style.textColor = colors.HexColor("#4B0082")  # Color púrpura oscuro
        title_style.fontSize = 18
        title_paragraph = Paragraph(titulo, title_style)

        # Configuración de la tabla
        table_data = [encabezados] + filas  # Encabezados + filas de datos
        table = Table(table_data, colWidths=[2 * inch, 2 * inch, 2 * inch, 2 * inch])  # Ancho ajustado a 4 columnas

        # Estilos de la tabla
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B0082")),  # Fondo púrpura para encabezados
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texto blanco para encabezados
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación centrada para todos los elementos
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Negrita en encabezados
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior en encabezados
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Fondo gris claro en filas
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray)  # Bordes grises en toda la tabla
        ])
        table.setStyle(table_style)

        # Construcción del PDF
        elements = [title_paragraph, table]
        doc.build(elements)
        messagebox.showinfo("PDF Exportado", f"El reporte '{titulo}' ha sido exportado como '{nombre_archivo}' en la carpeta 'reports'.")

    def mostrar_prestamos_vencidos(self):
        resultado = prestamo_controller.listar_prestamos_vencidos()
        if resultado:
            encabezados = ["ID", "Usuario", "Libro", "Fecha Préstamo"]
            filas = [[row[0], row[1], row[2], row[3]] for row in resultado]
            reporte = "\n".join([f"ID: {row[0]}, Usuario: {row[1]}, Libro: {row[2]}, Fecha Préstamo: {row[3]}" for row in resultado])
        else:
            encabezados = ["ID", "Usuario", "Libro", "Fecha Préstamo"]
            reporte = "No hay préstamos vencidos."
            filas = [["Sin datos", "", "", ""]]
        messagebox.showinfo("Préstamos Vencidos", reporte)
        self.generar_pdf("Préstamos Vencidos", encabezados, filas, "prestamos_vencidos.pdf")
        resultado = prestamo_controller.listar_prestamos_vencidos()
        self.generar_pdf("Préstamos Vencidos", reporte, "prestamos_vencidos.pdf")

    def mostrar_libros_mas_prestados(self):
        resultado = prestamo_controller.libros_mas_prestados_ultimo_mes()
        if resultado:
            encabezados = ["Libro", "Total Préstamos"]
            filas = [[row[0], row[1]] for row in resultado]
            reporte = "\n".join([f"Libro: {row[0]}, Total Préstamos: {row[1]}" for row in resultado])
        else:
            reporte = "No hay datos de préstamos en el último mes."
            filas = [["Sin datos", ""]]
        messagebox.showinfo("Libros Más Prestados", reporte)
        self.generar_pdf("Libros Más Prestados Último Mes", encabezados, filas, "libros_mas_prestados.pdf")

    def mostrar_usuarios_mas_prestamos(self):
        resultado = prestamo_controller.usuarios_mas_prestamos()
        if resultado:
            encabezados = ["Usuario", "Total Préstamos"]
            filas = [[row[0], row[1]] for row in resultado]
            reporte = "\n".join([f"Usuario: {row[0]}, Total Préstamos: {row[1]}" for row in resultado])
        else:
            reporte = "No hay datos de préstamos para los usuarios."
            filas = [["Sin datos", ""]]
        messagebox.showinfo("Usuarios con Más Préstamos", reporte)
        self.generar_pdf("Usuarios con Más Préstamos", encabezados, filas, "usuarios_mas_prestamos.pdf")


if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
