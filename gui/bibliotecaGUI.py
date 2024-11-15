import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import webbrowser
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
        self.root.attributes('-fullscreen', True)  # Activar pantalla completa

        bg_image = Image.open("./gui/libraryBg.jpg")
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title_label = tk.Label(
            self.root,
            text="Menú de Opciones",
            font=("Helvetica", 16, "bold"),
            bg="#FFFFFF",  # Fondo del título para que sea visible
            fg="#000000"  # Color de texto del título
        )
        title_label.pack(side=tk.TOP, pady=(20, 10))

        # Crear botones en columna
        self.create_buttons()
class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.attributes('-fullscreen', True)  # Activate full screen

        # Load background image and adjust size
        bg_image = Image.open("./gui/libraryBg.jpg")
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Background image label
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label at the top
        title_label = tk.Label(
            self.root,
            text="Menú de Opciones",
            font=("Helvetica", 20, "bold"),  # Increased font size
            bg="#FFFFFF",
            fg="#000000"
        )
        title_label.pack(side=tk.TOP, pady=(200, 10))

        # Frame to hold buttons, centered vertically and horizontally
        self.button_container = tk.Frame(self.root)
        self.button_container.place(relx=0.5, rely=0.5, anchor="center")

        # Create buttons in three columns
        self.create_buttons()

    def create_buttons(self):
        # Three lists of buttons for three columns
        column1 = [
            ("Registro de Autores", self.open_autores_window),
            ("Registro de Libros", self.open_libros_window),
            ("Registro de Usuarios", self.open_usuarios_window),
        ]

        column2 = [
            ("Consultar Préstamos", self.open_prestamos_activos_window),
            ("Registrar Préstamo", self.open_prestamo_window),
            ("Devolución de Libros", self.open_devolucion_window),
            ("Reportes", self.open_reportes_window),
        ]

        column3 = [
            ("Consulta de Libros", self.open_consulta_libros_window),
            ("Consulta de Autores", self.open_consulta_autores_window),
            ("Consulta de Usuarios", self.open_consulta_usuarios_window),
        ]

        # Adding buttons to each column with increased font size and no background in container
        for row, (text, command) in enumerate(column1):
            button = tk.Button(self.button_container, text=text, command=command, width=25, height=3, font=("Helvetica", 14))
            button.grid(row=row, column=0, padx=10, pady=5)

        for row, (text, command) in enumerate(column2):
            button = tk.Button(self.button_container, text=text, command=command, width=25, height=3, font=("Helvetica", 14))
            button.grid(row=row, column=1, padx=10, pady=5)

        for row, (text, command) in enumerate(column3):
            button = tk.Button(self.button_container, text=text, command=command, width=25, height=3, font=("Helvetica", 14))
            button.grid(row=row, column=2, padx=10, pady=5)

 
    def set_window_background(self, window):
        """Función utilitaria para agregar fondo a las ventanas secundarias."""
        bg_label = tk.Label(window, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def open_autores_window(self):
        # Ventana para registrar autores
        autores_window = tk.Toplevel(self.root)
        autores_window.title("Registro de Autores")
        autores_window.geometry("400x300")

        self.set_window_background(autores_window)


        frame = tk.Frame(autores_window)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        nombre_autor = tk.Entry(frame)
        nombre_autor.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        apellido_autor = tk.Entry(frame)
        apellido_autor.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Nacionalidad:").grid(row=2, column=0, padx=5, pady=5)
        nacionalidad_autor = tk.Entry(frame)
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
        
        tk.Button(frame, text="Registrar Autor", command=registrar_autor).grid(row=3, columnspan=2, pady=10)

    def open_libros_window(self):
        # Ventana para registrar libros
        libros_window = tk.Toplevel(self.root)
        libros_window.title("Registro de Libros")
        libros_window.geometry("400x400")

        self.set_window_background(libros_window)

        # Marco centralizado
        frame = tk.Frame(libros_window)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
        isbn_libro = tk.Entry(frame)
        isbn_libro.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Título:").grid(row=1, column=0, padx=5, pady=5)
        titulo_libro = tk.Entry(frame)
        titulo_libro.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Género:").grid(row=2, column=0, padx=5, pady=5)
        genero_libro = ttk.Combobox(frame, values=["Ficción", "Terror", "Filosofía", "Novela", "Aventura", "Drama"], state="readonly", width=18)
        genero_libro.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Año de Publicación:").grid(row=3, column=0, padx=5, pady=5)
        anio_libro = tk.Entry(frame)
        anio_libro.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Cantidad Disponible:").grid(row=4, column=0, padx=5, pady=5)
        cantidad_libro = tk.Entry(frame)
        cantidad_libro.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="ID del Autor:").grid(row=5, column=0, padx=5, pady=5)
        autor_id_libro = tk.Entry(frame)
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

        tk.Button(frame, text="Registrar Libro", command=registrar_libro).grid(row=6, columnspan=2, pady=10)

    def open_consulta_usuarios_window(self):
        consulta_window = tk.Toplevel(self.root)
        consulta_window.title("Consultar Usuarios")
        consulta_window.geometry("1000x400")

        self.set_window_background(consulta_window)

        tk.Label(consulta_window, text="Buscar por Nombre o Apellido:").pack(pady=10)
        criterio_entry = tk.Entry(consulta_window, width=30)
        criterio_entry.pack(pady=5)

        columns = ("ID", "Nombre", "Apellido", "Tipo de Usuario", "Dirección", "Teléfono")
        resultado_tree = ttk.Treeview(consulta_window, columns=columns, show="headings", height=15)
        resultado_tree.heading("ID", text="ID")
        resultado_tree.heading("Nombre", text="Nombre")
        resultado_tree.heading("Apellido", text="Apellido")
        resultado_tree.heading("Tipo de Usuario", text="Tipo de Usuario")
        resultado_tree.heading("Dirección", text="Dirección")
        resultado_tree.heading("Teléfono", text="Teléfono")

        resultado_tree.column("ID", width=50, anchor="center")
        resultado_tree.column("Nombre", width=150, anchor="center")
        resultado_tree.column("Apellido", width=150, anchor="center")
        resultado_tree.column("Tipo de Usuario", width=150, anchor="center")
        resultado_tree.column("Dirección", width=200, anchor="center")
        resultado_tree.column("Teléfono", width=150, anchor="center")
        resultado_tree.pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview", rowheight=32, font=("Helvetica", 15), foreground="black")
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))

        resultado_tree.tag_configure("oddrow", background="#f0f0f0")
        resultado_tree.tag_configure("evenrow", background="#ffffff")

        def buscar_usuarios():
            criterio = criterio_entry.get()
            if criterio:
                resultados = usuario_controller.buscar_usuarios_por_nombre(criterio)
                for item in resultado_tree.get_children():
                    resultado_tree.delete(item)

                if resultados:
                    for index, resultado in enumerate(resultados):
                        tag = "oddrow" if index % 2 == 0 else "evenrow"
                        resultado_tree.insert("", "end", values=resultado, tags=(tag,))
                else:
                    resultado_tree.insert("", "end", values=("No se encontraron usuarios", "", "", "", "", ""), tags=("oddrow",))

        tk.Button(consulta_window, text="Buscar", command=buscar_usuarios).pack(pady=5)


    def open_usuarios_window(self):
        # Ventana para registrar usuarios
        usuarios_window = tk.Toplevel(self.root)
        usuarios_window.title("Registro de Usuarios")
        usuarios_window.geometry("400x300")

        # Configurar el fondo de la ventana
        self.set_window_background(usuarios_window)
        
        # Marco centralizado
        frame = tk.Frame(usuarios_window)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Agregar campos dentro del marco sin modificar colores
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        nombre_usuario = tk.Entry(frame)
        nombre_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
        apellido_usuario = tk.Entry(frame)
        apellido_usuario.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Tipo de Usuario:").grid(row=2, column=0, padx=5, pady=5)
        tipo_usuario = ttk.Combobox(frame, values=["estudiante", "profesor"], state="readonly", width=18)
        tipo_usuario.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
        direccion_usuario = tk.Entry(frame)
        direccion_usuario.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Teléfono:").grid(row=4, column=0, padx=5, pady=5)
        telefono_usuario = tk.Entry(frame)
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

        tk.Button(frame, text="Registrar Usuario", command=registrar_usuario).grid(row=5, columnspan=2, pady=10)

    def open_consulta_libros_window(self):
        # Ventana para consultar libros
        consulta_window = tk.Toplevel(self.root)
        consulta_window.title("Consultar Libros")
        consulta_window.geometry("1000x700")  # Ajuste del ancho y alto de la ventana

        self.set_window_background(consulta_window)

        tk.Label(consulta_window, text="Buscar por ISBN o Título:").pack(pady=10)
        criterio_entry = tk.Entry(consulta_window, width=30)
        criterio_entry.pack(pady=5)

        # Crear el Treeview para mostrar los resultados en forma de tabla
        columns = ("ISBN", "Título", "Género", "Año de Publicación", "Autor", "Cantidad Disponible")
        resultado_tree = ttk.Treeview(consulta_window, columns=columns, show="headings", height=15)
        resultado_tree.heading("ISBN", text="ISBN")
        resultado_tree.heading("Título", text="Título")
        resultado_tree.heading("Género", text="Género")
        resultado_tree.heading("Año de Publicación", text="Año de Publicación")
        resultado_tree.heading("Autor", text="Autor")  # Cambiado a Autor
        resultado_tree.heading("Cantidad Disponible", text="Cantidad Disponible")

        # Configurar el ancho de las columnas y centrado horizontal
        resultado_tree.column("ISBN", width=150, anchor="center")
        resultado_tree.column("Título", width=250, anchor="center")
        resultado_tree.column("Género", width=150, anchor="center")
        resultado_tree.column("Año de Publicación", width=150, anchor="center")
        resultado_tree.column("Autor", width=200, anchor="center")  # Ajustar el ancho para el nombre completo
        resultado_tree.column("Cantidad Disponible", width=180, anchor="center")
        resultado_tree.pack(pady=10)

        # Estilos para ajustar el tamaño de fuente y centrado de filas
        style = ttk.Style()
        style.configure("Treeview", rowheight=32, font=("Helvetica", 15), foreground="black")  # Aumenta el tamaño de la fuente
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))

        # Alternar colores de filas
        resultado_tree.tag_configure("oddrow", background="#f0f0f0")
        resultado_tree.tag_configure("evenrow", background="#ffffff")

        def buscar_libros():
            criterio = criterio_entry.get()
            if criterio:
                resultados = libro_controller.buscar_libros(criterio)
                # Limpiar resultados anteriores
                for item in resultado_tree.get_children():
                    resultado_tree.delete(item)

                if resultados:
                    for index, resultado in enumerate(resultados):
                        isbn, titulo, genero, anio_publicacion, autor_nombre, cantidad_disponible = resultado
                        # Alternar etiquetas para las filas
                        tag = "oddrow" if index % 2 == 0 else "evenrow"
                        resultado_tree.insert("", "end", values=(isbn, titulo, genero, anio_publicacion, autor_nombre, cantidad_disponible), tags=(tag,))
                else:
                    resultado_tree.insert("", "end", values=("No se encontraron libros", "", "", "", "", ""), tags=("oddrow",))

        tk.Button(consulta_window, text="Buscar", command=buscar_libros).pack(pady=5)


    def open_consulta_autores_window(self):
        consulta_window = tk.Toplevel(self.root)
        consulta_window.title("Consultar Autores")
        consulta_window.geometry("1000x400")

        self.set_window_background(consulta_window)

        tk.Label(consulta_window, text="Buscar por Nombre o Apellido:").pack(pady=10)
        criterio_entry = tk.Entry(consulta_window, width=30)
        criterio_entry.pack(pady=5)

        columns = ("ID", "Nombre", "Apellido", "Nacionalidad")
        resultado_tree = ttk.Treeview(consulta_window, columns=columns, show="headings", height=15)
        resultado_tree.heading("ID", text="ID")
        resultado_tree.heading("Nombre", text="Nombre")
        resultado_tree.heading("Apellido", text="Apellido")
        resultado_tree.heading("Nacionalidad", text="Nacionalidad")

        resultado_tree.column("ID", width=190, anchor="center")
        resultado_tree.column("Nombre", width=200, anchor="center")
        resultado_tree.column("Apellido", width=200, anchor="center")
        resultado_tree.column("Nacionalidad", width=200, anchor="center")
        resultado_tree.pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview", rowheight=32, font=("Helvetica", 15), foreground="black")
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))

        resultado_tree.tag_configure("oddrow", background="#f0f0f0")
        resultado_tree.tag_configure("evenrow", background="#ffffff")

        def buscar_autores():
            criterio = criterio_entry.get()
            if criterio:
                resultados = autor_controller.buscar_autores_por_nombre(criterio)
                for item in resultado_tree.get_children():
                    resultado_tree.delete(item)

                if resultados:
                    for index, resultado in enumerate(resultados):
                        tag = "oddrow" if index % 2 == 0 else "evenrow"
                        resultado_tree.insert("", "end", values=resultado, tags=(tag,))
                else:
                    resultado_tree.insert("", "end", values=("No se encontraron autores", "", "", ""), tags=("oddrow",))

        tk.Button(consulta_window, text="Buscar", command=buscar_autores).pack(pady=5)

    def open_prestamos_activos_window(self):
        # Ventana para consultar préstamos activos
        prestamos_window = tk.Toplevel(self.root)
        prestamos_window.title("Consultar Préstamos")
        prestamos_window.geometry("1000x700")  # Tamaño de la ventana

        self.set_window_background(prestamos_window)

        # Etiqueta principal
        tk.Label(prestamos_window, text="Historial de Préstamos", font=("Helvetica", 18, "bold")).pack(pady=10)

        # Frame para centrar los contenidos
        frame = tk.Frame(prestamos_window, bg="#333333", padx=10, pady=10)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Crear el Treeview para mostrar los resultados
        columns = ("ID", "Usuario", "Libro", "Fecha Préstamo", "Fecha Devolución Estimada", "Fecha Devolución Real")
        resultado_tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        resultado_tree.heading("ID", text="ID")
        resultado_tree.heading("Usuario", text="Usuario")
        resultado_tree.heading("Libro", text="Libro")
        resultado_tree.heading("Fecha Préstamo", text="Fecha Préstamo")
        resultado_tree.heading("Fecha Devolución Estimada", text="Devolución Estimada")
        resultado_tree.heading("Fecha Devolución Real", text="Devolución Real")

        # Configurar columnas
        resultado_tree.column("ID", width=100, anchor="center")
        resultado_tree.column("Usuario", width=200, anchor="center")
        resultado_tree.column("Libro", width=200, anchor="center")
        resultado_tree.column("Fecha Préstamo", width=150, anchor="center")
        resultado_tree.column("Fecha Devolución Estimada", width=180, anchor="center")
        resultado_tree.column("Fecha Devolución Real", width=180, anchor="center")
        resultado_tree.pack(pady=10)

        # Estilos de las filas y encabezados
        style = ttk.Style()
        style.configure("Treeview", rowheight=32, font=("Helvetica", 15), foreground="black")
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))

        # Alternar colores de filas
        resultado_tree.tag_configure("oddrow", background="#f0f0f0")
        resultado_tree.tag_configure("evenrow", background="#ffffff")
        resultado_tree.tag_configure("no_data", background="#000000", foreground="#FFFFFF")  # Fondo negro, letra blanca

        try:
            prestamos = prestamo_controller.obtener_todos_los_prestamos()

            # Populate the Treeview
            if prestamos:
                for index, prestamo in enumerate(prestamos):
                    tag = "oddrow" if index % 2 == 0 else "evenrow"
                    resultado_tree.insert("", "end", values=prestamo, tags=(tag,))
            else:
                # If there are no loans, show a single row with a message
                resultado_tree.insert("", "end", values=("No hay préstamos registrados", "", "", "", "", ""), tags=("no_data",))

            # Configure tag for styling no-data message
            resultado_tree.tag_configure("no_data", background="#000000", foreground="#FFFFFF")  # Black background, white text
        except Exception as e:
            # Manejo de errores con fila unificada
            print(f"Error al obtener préstamos activos: {e}")
            resultado_tree.insert(
                "",
                "end",
                values=("No hay préstamos activos", "", "", "", "", ""),
                tags=("no_data",)
            )


    def open_prestamo_window(self):
        # Ventana para registrar un préstamo de libro
        prestamo_window = tk.Toplevel(self.root)
        prestamo_window.title("Registrar Préstamo de Libro")
        prestamo_window.geometry("400x300")

        # Configurar el fondo de pantalla
        self.set_window_background(prestamo_window)
        
        # Marco centralizado
        frame = tk.Frame(prestamo_window)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Agregar campos dentro del marco
        tk.Label(frame, text="Usuario ID:").grid(row=0, column=0, padx=5, pady=5)
        usuario_id_entry = tk.Entry(frame)
        usuario_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Libro ISBN:").grid(row=1, column=0, padx=5, pady=5)
        libro_isbn_entry = tk.Entry(frame)
        libro_isbn_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Fecha de Préstamo (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        fecha_prestamo = datetime.now().strftime("%Y-%m-%d")  # Fecha actual
        tk.Label(frame, text=fecha_prestamo).grid(row=2, column=1, padx=5, pady=5)  # Mostrar la fecha como un Label


        tk.Label(frame, text="Fecha de Devolución (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        fecha_devolucion_entry = tk.Entry(frame)
        fecha_devolucion_entry.grid(row=3, column=1, padx=5, pady=5)

        def registrar_prestamo():
            usuario_id = usuario_id_entry.get()
            libro_isbn = libro_isbn_entry.get()
            fecha_devolucion = fecha_devolucion_entry.get()

            if usuario_id.isdigit() and libro_isbn and self.validar_fecha(fecha_prestamo) and self.validar_fecha(fecha_devolucion):
                resultado = prestamo_controller.registrar_prestamo(int(usuario_id), libro_isbn, fecha_prestamo, fecha_devolucion)

                if resultado == "Éxito":
                    messagebox.showinfo("Éxito", "Préstamo registrado exitosamente", parent=prestamo_window)
                    usuario_id_entry.delete(0, tk.END)
                    libro_isbn_entry.delete(0, tk.END)
                    fecha_devolucion_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Advertencia", resultado, parent=prestamo_window)
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios y deben tener el formato correcto", parent=prestamo_window)

        tk.Button(frame, text="Registrar Préstamo", command=registrar_prestamo).grid(row=4, columnspan=2, pady=10)

    def open_devolucion_window(self):
        # Ventana para registrar una devolución de libro
        devolucion_window = tk.Toplevel(self.root)
        devolucion_window.title("Registrar Devolución de Libro")
        devolucion_window.geometry("400x250")

        # Configurar el fondo de pantalla
        self.set_window_background(devolucion_window)

        # Marco centralizado
        frame = tk.Frame(devolucion_window)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Agregar campos dentro del marco
        tk.Label(frame, text="Préstamo ID:").grid(row=0, column=0, padx=5, pady=5)
        prestamo_id_entry = tk.Entry(frame)
        prestamo_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Estado de Devolución:").grid(row=1, column=0, padx=5, pady=5)
        estado_combo = ttk.Combobox(frame, values=["en condiciones", "dañado"], state="readonly", width=18)
        estado_combo.grid(row=1, column=1, padx=5, pady=5)
        estado_combo.set("en condiciones")

        tk.Label(frame, text="Fecha Devolución Real (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        fecha_devolucion_real_entry = tk.Entry(frame)
        fecha_devolucion_real_entry.grid(row=2, column=1, padx=5, pady=5)
        fecha_devolucion_real_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to today's date

        def registrar_devolucion():
            prestamo_id = prestamo_id_entry.get()
            estado = estado_combo.get()
            fecha_devolucion_real = fecha_devolucion_real_entry.get()

            if prestamo_id.isdigit() and self.validar_fecha(fecha_devolucion_real):
                resultado = prestamo_controller.registrar_devolucion(int(prestamo_id), estado, fecha_devolucion_real)
                if resultado == "Éxito":
                    messagebox.showinfo("Éxito", "Devolución registrada exitosamente", parent=devolucion_window)
                    prestamo_id_entry.delete(0, tk.END)
                    estado_combo.set("en condiciones")
                    fecha_devolucion_real_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Advertencia", resultado, parent=devolucion_window)
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios y deben tener el formato correcto", parent=devolucion_window)

        tk.Button(frame, text="Registrar Devolución", command=registrar_devolucion).grid(row=3, columnspan=2, pady=10)


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

        # Configurar el fondo de pantalla
        self.set_window_background(reportes_window)

        # Marco centralizado
        frame = tk.Frame(reportes_window)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Botones de selección de reportes dentro del marco
        tk.Button(frame, text="Préstamos Vencidos", command=self.mostrar_prestamos_vencidos, width=30).pack(pady=10)
        tk.Button(frame, text="Libros Más Prestados Último Mes", command=self.mostrar_libros_mas_prestados, width=30).pack(pady=10)
        tk.Button(frame, text="Usuarios con Más Préstamos", command=self.mostrar_usuarios_mas_prestamos, width=30).pack(pady=10)

    def generar_pdf(self, titulo, encabezados, filas, nombre_archivo):
        # Obtener la ruta absoluta a la carpeta 'reports' en el directorio raíz
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports'))
        
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

        # Intentar abrir el PDF automáticamente según el sistema operativo
        try:
            if os.name == 'nt':  # Para sistemas Windows
                os.startfile(pdf_path)
            else:  # Para otros sistemas operativos (MacOS, Linux)
                print("Abriendo PDF automáticamente... en mac")
                subprocess.run(["open", pdf_path])
        except Exception as e:
            messagebox.showwarning("Error al abrir PDF", f"No se pudo abrir el archivo PDF automáticamente: {e}")

    def mostrar_prestamos_vencidos(self):
        resultado = prestamo_controller.listar_prestamos_vencidos()
        if resultado:
            encabezados = ["ID", "Usuario", "Libro", "Fecha Préstamo"]
            filas = [[row[0], row[1], row[2], row[3]] for row in resultado]
        else:
            encabezados = ["ID", "Usuario", "Libro", "Fecha Préstamo"]
            filas = [["Sin datos", "", "", ""]]
        self.generar_pdf("Préstamos Vencidos", encabezados, filas, "prestamos_vencidos.pdf")

    def mostrar_libros_mas_prestados(self):
        resultado = prestamo_controller.libros_mas_prestados_ultimo_mes()
        if resultado:
            encabezados = ["Libro", "Total Préstamos"]
            filas = [[row[0], row[1]] for row in resultado]
        else:
            encabezados = ["Libro", "Total Préstamos"]
            filas = [["Sin datos", ""]]
        self.generar_pdf("Libros Más Prestados Último Mes", encabezados, filas, "libros_mas_prestados.pdf")

    def mostrar_usuarios_mas_prestamos(self):
        resultado = prestamo_controller.usuarios_mas_prestamos()
        if resultado:
            encabezados = ["Usuario", "Total Préstamos"]
            filas = [[row[0], row[1]] for row in resultado]
        else:
            encabezados = ["Usuario", "Total Préstamos"]
            filas = [["Sin datos", ""]]
        self.generar_pdf("Usuarios con Más Préstamos", encabezados, filas, "usuarios_mas_prestamos.pdf")

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
