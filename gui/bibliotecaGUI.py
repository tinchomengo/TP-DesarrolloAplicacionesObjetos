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
from reportlab.lib.pagesizes import landscape
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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
            text="Gestor de Biblioteca",
            font=("Helvetica", 30, "bold"),  # Increased font size
            bg="#000000",
            fg="#FFFFFF"
        )
        title_label.pack(side=tk.TOP, pady=(200, 10))

        # Frame to hold buttons, centered vertically and horizontally
        self.button_container = tk.Frame(self.root)
        self.button_container.place(relx=0.5, rely=0.5, anchor="center")

        # Create buttons in three columns
        self.create_buttons()

                # Button to close the application
        close_button = tk.Button(
            self.root,
            text="Cerrar aplicación",
            command=self.cerrar_aplicacion,
            width=20,
            height=2,
            font=("Helvetica", 14),
            bg="#FF4C4C",  # Red background for emphasis
            fg="black"
        )
        close_button.place(relx=0.5, rely=0.9, anchor="center")  # Position the button at the bottom

    
    def cerrar_aplicacion(self):
        """Cierra todas las ventanas y termina el programa."""
        if messagebox.askyesno("Confirm", "Are you sure you want to close the app?"):
            self.root.destroy()
            sys.exit()

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
        libros_window.geometry("500x500")

        self.set_window_background(libros_window)

        # Marco centralizado
        frame = tk.Frame(libros_window)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Obtener autores de la base de datos
        autores = autor_controller.buscar_autores_por_nombre("")  # Buscar todos los autores
        autores_opciones = [f"{autor[1]} {autor[2]}" for autor in autores]  # Nombre + Apellido
        autores_dict = {f"{autor[1]} {autor[2]}": autor[0] for autor in autores}  # {Nombre: ID}

        # Campos para ingresar los datos del libro
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

        # Dropdown para seleccionar autor
        tk.Label(frame, text="Seleccionar Autor:").grid(row=5, column=0, padx=5, pady=5)
        autor_dropdown = ttk.Combobox(frame, values=autores_opciones, state="readonly", width=18)
        autor_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Label y botón en la misma fila que el dropdown
        tk.Label(frame, text="Autor no listado?").grid(row=5, column=2, padx=5, pady=5, sticky="e")
        tk.Button(frame, text="Registrar", command=self.open_autores_window, width=10, height=1).grid(row=5, column=3, padx=5, pady=5)

        def registrar_libro():
            isbn = isbn_libro.get()
            titulo = titulo_libro.get()
            genero = genero_libro.get()
            anio = anio_libro.get()
            cantidad = cantidad_libro.get()
            autor_seleccionado = autor_dropdown.get()

            if autor_seleccionado and autor_seleccionado in autores_dict:
                autor_id = autores_dict[autor_seleccionado]  # Obtener el ID del autor seleccionado
            else:
                autor_id = None  # Si no hay autor seleccionado, marcar como None

            if isbn and titulo and genero and anio.isdigit() and cantidad.isdigit() and autor_id:
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
                    autor_dropdown.set("")
                elif resultado == "Año inválido":
                    messagebox.showwarning("Advertencia", "El año de publicación no puede ser mayor al año actual.", parent=libros_window)
                elif resultado == "Cantidad inválida":
                    messagebox.showwarning("Advertencia", "La cantidad disponible debe ser mayor a 0.", parent=libros_window)
                elif resultado == "ISBN duplicado":
                    messagebox.showwarning("Advertencia", "El ISBN ya existe en la base de datos.", parent=libros_window)
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios y deben tener el formato correcto.", parent=libros_window)

        tk.Button(frame, text="Registrar Libro", command=registrar_libro).grid(row=6, columnspan=4, pady=10)

    def open_consulta_usuarios_window(self):
        consulta_window = tk.Toplevel(self.root)
        consulta_window.title("Consultar Usuarios")
        consulta_window.geometry("1000x500")

        self.set_window_background(consulta_window)

        # Encabezado y entrada para búsqueda
        frame_top = tk.Frame(consulta_window)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Buscar por Nombre o Apellido:").grid(row=0, column=0, padx=5)
        criterio_entry = tk.Entry(frame_top, width=30)
        criterio_entry.grid(row=0, column=1, padx=5)
        tk.Button(frame_top, text="Buscar", command=lambda: buscar_usuarios()).grid(row=0, column=2, padx=5)

        # Configuración de tabla
        columns = ("ID", "Nombre", "Apellido", "Tipo de Usuario", "Dirección", "Teléfono", "Multa")
        resultado_tree = ttk.Treeview(consulta_window, columns=columns, show="headings", height=15)
        for col in columns:
            resultado_tree.heading(col, text=col)
            resultado_tree.column(col, width=150, anchor="center")
        resultado_tree.column("ID", width=50, anchor="center")
        resultado_tree.column("Multa", width=100, anchor="center")
        resultado_tree.pack(pady=10)

        # Estilos
        style = ttk.Style()
        style.configure("Treeview", rowheight=32, font=("Helvetica", 15), foreground="black")
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))

        resultado_tree.tag_configure("oddrow", background="#f0f0f0")
        resultado_tree.tag_configure("evenrow", background="#ffffff")


        # Función para cargar datos
        def cargar_usuarios(usuarios):
            for item in resultado_tree.get_children():
                resultado_tree.delete(item)

            if usuarios:
                for index, usuario in enumerate(usuarios):
                    tag = "oddrow" if index % 2 == 0 else "evenrow"
                    resultado_tree.insert(
                        "",
                        "end",
                        values=usuario,
                        tags=(tag,)
                    )
            else:
                resultado_tree.insert("", "end", values=("No se encontraron usuarios", "", "", "", "", "", ""), tags=("oddrow",))

        # Función para eliminar usuario
        def eliminar_usuario(usuario_id):
            confirm = messagebox.askyesno("Confirmar Baja", f"¿Está seguro de eliminar el usuario ID {usuario_id}?")
            if confirm:
                resultado = usuario_controller.eliminar_usuario(usuario_id)
                if resultado == "Éxito":
                    messagebox.showinfo("Éxito", f"El usuario ID {usuario_id} ha sido eliminado.")
                    usuarios = usuario_controller.buscar_usuarios_por_nombre("")
                    cargar_usuarios(usuarios)
                elif resultado == "El usuario tiene préstamos activos. No se puede eliminar.":
                    messagebox.showwarning("Advertencia", resultado)
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el usuario.")

        # Evento para clic en la columna Baja
        def on_item_click(event):
            item_id = resultado_tree.identify_row(event.y)
            column = resultado_tree.identify_column(event.x)
            if column == "#7":  # Columna "Baja"
                usuario_id = resultado_tree.item(item_id)["values"][0]
                if usuario_id:
                    eliminar_usuario(usuario_id)

        resultado_tree.bind("<Button-1>", on_item_click)

        # Función para buscar usuarios
        def buscar_usuarios():
            criterio = criterio_entry.get()
            usuarios = usuario_controller.buscar_usuarios_por_nombre(criterio)
            cargar_usuarios(usuarios)

        # Botón para registrar nuevo usuario
        tk.Button(consulta_window, text="Registrar Nuevo Usuario", command=self.open_usuarios_window,font=("Helvetica", 14),
            bg="#4CAF50",
            fg="black",
            width=25,
            height=2
        ).pack(pady=20, side=tk.BOTTOM)

        # Cargar todos los usuarios al abrir la ventana
        usuarios = usuario_controller.buscar_usuarios_por_nombre("")
        cargar_usuarios(usuarios)


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

        # Frame superior para la búsqueda
        frame_top = tk.Frame(consulta_window)
        frame_top.pack(pady=10)

        # Campo de entrada y botón de búsqueda en la misma fila
        tk.Label(frame_top, text="Buscar por ISBN o Título:").grid(row=0, column=0, padx=5)
        criterio_entry = tk.Entry(frame_top, width=30)
        criterio_entry.grid(row=0, column=1, padx=5)
        tk.Button(frame_top, text="Buscar", command=lambda: buscar_libros()).grid(row=0, column=2, padx=5)

        # Crear el Treeview para mostrar los resultados en forma de tabla
        columns = ("ISBN", "Título", "Género", "Año de Publicación", "Autor", "Cantidad Disponible", "Baja")
        resultado_tree = ttk.Treeview(consulta_window, columns=columns, show="headings", height=15)
        for col in columns:
            resultado_tree.heading(col, text=col)
            resultado_tree.column(col, anchor="center")
        resultado_tree.column("ISBN", width=150, anchor="center")
        resultado_tree.column("Título", width=250, anchor="center")
        resultado_tree.column("Género", width=150, anchor="center")
        resultado_tree.column("Año de Publicación", width=150, anchor="center")
        resultado_tree.column("Autor", width=200, anchor="center")
        resultado_tree.column("Cantidad Disponible", width=180, anchor="center")
        resultado_tree.column("Baja", width=50, anchor="center")
        resultado_tree.pack(pady=10)

        # Estilos para ajustar el tamaño de fuente y centrado de filas
        style = ttk.Style()
        style.configure("Treeview", rowheight=32, font=("Helvetica", 15), foreground="black")
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))

        # Alternar colores de filas
        resultado_tree.tag_configure("oddrow", background="#f0f0f0")
        resultado_tree.tag_configure("evenrow", background="#ffffff")

        # Función para cargar libros en el Treeview
        def cargar_libros(libros):
            for item in resultado_tree.get_children():
                resultado_tree.delete(item)

            if libros:
                for index, libro in enumerate(libros):
                    tag = "oddrow" if index % 2 == 0 else "evenrow"
                    resultado_tree.insert(
                        "",
                        "end",
                        values=(*libro, "-"),  # Agregar "-" en la columna "Baja"
                        tags=(tag,)
                    )
            else:
                resultado_tree.insert("", "end", values=("No se encontraron libros", "", "", "", "", "", ""), tags=("oddrow",))

        # Función para eliminar libro
        def eliminar_libro(isbn):
            confirm = messagebox.askyesno("Confirmar Baja", f"¿Está seguro de eliminar el libro con ISBN {isbn}?")
            if confirm:
                resultado = libro_controller.eliminar_libro(isbn)
                if resultado == "Éxito":
                    messagebox.showinfo("Éxito", f"El libro con ISBN {isbn} ha sido eliminado.")
                    libros = libro_controller.buscar_libros("")  # Recargar lista completa
                    cargar_libros(libros)
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el libro.")

        # Evento para clic en la columna Baja
        def on_item_click(event):
            item_id = resultado_tree.identify_row(event.y)
            column = resultado_tree.identify_column(event.x)
            if column == "#7":  # Columna "Baja"
                isbn = resultado_tree.item(item_id)["values"][0]
                if isbn:
                    eliminar_libro(isbn)

        resultado_tree.bind("<Button-1>", on_item_click)

        # Función para buscar libros
        def buscar_libros():
            criterio = criterio_entry.get()
            libros = libro_controller.buscar_libros(criterio)
            cargar_libros(libros)

        # Botón para registrar nuevo libro
        tk.Button(consulta_window, text="Registrar Nuevo Libro", command=self.open_libros_window).pack(pady=10)

        # Cargar todos los libros al abrir la ventana
        libros = libro_controller.buscar_libros("")
        cargar_libros(libros)

    def open_consulta_autores_window(self):
        consulta_window = tk.Toplevel(self.root)
        consulta_window.title("Consultar Autores")
        consulta_window.geometry("1000x500")  # Ajustar tamaño para espacio adicional

        self.set_window_background(consulta_window)

        # Frame superior para la búsqueda
        frame_top = tk.Frame(consulta_window)
        frame_top.pack(pady=10)

        # Campo de entrada y botón de búsqueda en la misma fila
        tk.Label(frame_top, text="Buscar por Nombre o Apellido:").grid(row=0, column=0, padx=5)
        criterio_entry = tk.Entry(frame_top, width=30)
        criterio_entry.grid(row=0, column=1, padx=5)
        tk.Button(frame_top, text="Buscar", command=lambda: buscar_autores()).grid(row=0, column=2, padx=5)

        # Crear el Treeview para mostrar los resultados en forma de tabla
        columns = ("ID", "Nombre", "Apellido", "Nacionalidad")
        resultado_tree = ttk.Treeview(consulta_window, columns=columns, show="headings", height=15)
        for col in columns:
            resultado_tree.heading(col, text=col)
            resultado_tree.column(col, anchor="center")
        resultado_tree.column("ID", width=100, anchor="center")
        resultado_tree.column("Nombre", width=200, anchor="center")
        resultado_tree.column("Apellido", width=200, anchor="center")
        resultado_tree.column("Nacionalidad", width=200, anchor="center")
        resultado_tree.pack(pady=10)

        # Estilos para ajustar el tamaño de fuente y centrado de filas
        style = ttk.Style()
        style.configure("Treeview", rowheight=32, font=("Helvetica", 15), foreground="black")
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))

        resultado_tree.tag_configure("oddrow", background="#f0f0f0")
        resultado_tree.tag_configure("evenrow", background="#ffffff")

        # Función para cargar datos en el Treeview
        def cargar_autores(autores):
            for item in resultado_tree.get_children():
                resultado_tree.delete(item)

            if autores:
                for index, autor in enumerate(autores):
                    tag = "oddrow" if index % 2 == 0 else "evenrow"
                    resultado_tree.insert(
                        "",
                        "end",
                        values=autor,
                        tags=(tag,)
                    )
            else:
                resultado_tree.insert("", "end", values=("No se encontraron autores", "", "", ""), tags=("oddrow",))

        # Función para buscar autores
        def buscar_autores():
            criterio = criterio_entry.get()
            autores = autor_controller.buscar_autores_por_nombre(criterio)
            cargar_autores(autores)

        # Botón para registrar un nuevo autor
        tk.Button(
            consulta_window,
            text="Registrar Nuevo Autor",
            command=self.open_autores_window,
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="black",
            width=25,
            height=2
        ).pack(pady=20, side=tk.BOTTOM)

        # Cargar todos los autores al abrir la ventana
        autores = autor_controller.buscar_autores_por_nombre("")
        cargar_autores(autores)


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
        columns = ("ID", "Usuario", "Libro", "Fecha Préstamo", "Fecha Devolución Estimada", "Fecha Devolución Real", "Baja")
        resultado_tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        resultado_tree.heading("ID", text="ID")
        resultado_tree.heading("Usuario", text="Usuario")
        resultado_tree.heading("Libro", text="Libro")
        resultado_tree.heading("Fecha Préstamo", text="Fecha Préstamo")
        resultado_tree.heading("Fecha Devolución Estimada", text="Devolución Estimada")
        resultado_tree.heading("Fecha Devolución Real", text="Devolución Real")
        resultado_tree.heading("Baja", text="Baja")

        # Configurar columnas
        resultado_tree.column("ID", width=100, anchor="center")
        resultado_tree.column("Usuario", width=200, anchor="center")
        resultado_tree.column("Libro", width=200, anchor="center")
        resultado_tree.column("Fecha Préstamo", width=150, anchor="center")
        resultado_tree.column("Fecha Devolución Estimada", width=150, anchor="center")
        resultado_tree.column("Fecha Devolución Real", width=150, anchor="center")
        resultado_tree.column("Baja", width=50, anchor="center")
        resultado_tree.pack(pady=10)

        # Estilos de las filas y encabezados
        style = ttk.Style()
        style.configure("Treeview", rowheight=32, font=("Helvetica", 15), foreground="black")
        style.configure("Treeview.Heading", font=("Helvetica", 13, "bold"))

        # Alternar colores de filas
        resultado_tree.tag_configure("oddrow", background="#f0f0f0")
        resultado_tree.tag_configure("evenrow", background="#ffffff")

        def eliminar_prestamo(prestamo_id):
            # Confirmar acción con el usuario
            confirm = messagebox.askyesno("Confirmar Baja", f"¿Está seguro de eliminar el préstamo ID {prestamo_id}?")
            if confirm:
                try:
                    # Llamar al controlador para eliminar el préstamo
                    resultado = prestamo_controller.eliminar_prestamo(prestamo_id)
                    if resultado == "Éxito":
                        messagebox.showinfo("Éxito", f"El préstamo ID {prestamo_id} ha sido eliminado.")
                        prestamos = prestamo_controller.obtener_todos_los_prestamos()
                        cargar_prestamos(prestamos)  # Recargar tabla
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el préstamo.")
                except Exception as e:
                    print(f"Error al eliminar préstamo: {e}")
                    messagebox.showerror("Error", "Ocurrió un error al intentar eliminar el préstamo.")

        def cargar_prestamos(prestamos):
            # Limpiar resultados anteriores
            for item in resultado_tree.get_children():
                resultado_tree.delete(item)

            if prestamos:
                for index, prestamo in enumerate(prestamos):
                    tag = "oddrow" if index % 2 == 0 else "evenrow"
                    resultado_tree.insert(
                        "",
                        "end",
                        values=(prestamo[0], prestamo[1], prestamo[2], prestamo[3], prestamo[4], prestamo[5], "-"),
                        tags=(tag,)
                    )
            else:
                resultado_tree.insert("", "end", values=("No hay préstamos registrados", "", "", "", "", "", ""), tags=("no_data",))

        def on_item_click(event):
            # Obtener el ítem clickeado
            item_id = resultado_tree.identify_row(event.y)
            column = resultado_tree.identify_column(event.x)
            if column == "#7":  # Columna "Baja"
                prestamo_id = resultado_tree.item(item_id)["values"][0]
                eliminar_prestamo(prestamo_id)

        # Asignar evento de clic en el Treeview
        resultado_tree.bind("<Button-1>", on_item_click)

        try:
            prestamos = prestamo_controller.obtener_todos_los_prestamos()
            cargar_prestamos(prestamos)
        except Exception as e:
            print(f"Error al obtener préstamos activos: {e}")
            resultado_tree.insert("", "end", values=("No hay préstamos activos", "", "", "", "", "", ""), tags=("no_data",))
        # Botón para registrar nuevo préstamo
        tk.Button(
            prestamos_window,
            text="Registrar Nuevo Préstamo",
            command=self.open_prestamo_window,
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="black",
            width=25,
            height=2
        ).pack(pady=20, side=tk.BOTTOM)


    def open_prestamo_window(self):
        # Ventana para registrar un préstamo de libro
        prestamo_window = tk.Toplevel(self.root)
        prestamo_window.title("Registrar Préstamo de Libro")
        prestamo_window.geometry("500x400")

        self.set_window_background(prestamo_window)

        # Obtener usuarios y libros
        usuarios = usuario_controller.buscar_usuarios_por_nombre("")  # Buscar todos los usuarios
        libros = libro_controller.buscar_libros("")  # Buscar todos los libros

        # Crear listas con nombres de usuarios y títulos de libros
        usuarios_opciones = [f"{usuario[1]} {usuario[2]}" for usuario in usuarios]  # Nombre + Apellido
        libros_opciones = [libro[1] for libro in libros]  # Título del libro

        # Diccionarios para mapear nombres/títulos con sus IDs/ISBNs
        usuarios_dict = {f"{usuario[1]} {usuario[2]}": usuario[0] for usuario in usuarios}  # {Nombre: ID}
        libros_dict = {libro[1]: libro[0] for libro in libros}  # {Título: ISBN}

        # Marco centralizado
        frame = tk.Frame(prestamo_window)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Seleccionar usuario
        tk.Label(frame, text="Seleccionar Usuario:").grid(row=0, column=0, padx=5, pady=5)
        usuario_dropdown = ttk.Combobox(frame, values=usuarios_opciones, state="readonly", width=25)
        usuario_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Seleccionar libro
        tk.Label(frame, text="Seleccionar Libro:").grid(row=1, column=0, padx=5, pady=5)
        libro_dropdown = ttk.Combobox(frame, values=libros_opciones, state="readonly", width=25)
        libro_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Fecha de préstamo
        tk.Label(frame, text="Fecha de Préstamo (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        fecha_prestamo = datetime.now().strftime("%Y-%m-%d")
        tk.Label(frame, text=fecha_prestamo).grid(row=2, column=1, padx=5, pady=5)

        # Fecha de devolución estimada
        tk.Label(frame, text="Fecha de Devolución (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        fecha_devolucion_entry = tk.Entry(frame)
        fecha_devolucion_entry.grid(row=3, column=1, padx=5, pady=5)

        def registrar_prestamo():
            usuario_seleccionado = usuario_dropdown.get()
            libro_seleccionado = libro_dropdown.get()
            fecha_devolucion = fecha_devolucion_entry.get()

            if usuario_seleccionado and libro_seleccionado and self.validar_fecha(fecha_devolucion):
                usuario_id = usuarios_dict[usuario_seleccionado]
                libro_isbn = libros_dict[libro_seleccionado]

                resultado = prestamo_controller.registrar_prestamo(usuario_id, libro_isbn, fecha_prestamo, fecha_devolucion)
                if resultado == "Éxito":
                    messagebox.showinfo("Éxito", "Préstamo registrado exitosamente", parent=prestamo_window)
                    usuario_dropdown.set("")
                    libro_dropdown.set("")
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
        reportes_window.geometry("500x400")  # Tamaño ajustado

        self.set_window_background(reportes_window)

        frame = tk.Frame(reportes_window)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Dropdown para elegir el tipo de reporte
        tk.Label(frame, text="Seleccionar Tipo de Reporte:", font=("Helvetica", 12)).pack(pady=10)
        reporte_tipo = ttk.Combobox(frame, values=["Tabular", "Gráfico"], state="readonly", width=20)
        reporte_tipo.pack(pady=5)
        reporte_tipo.set("Tabular")  # Valor por defecto

        # Botones para generar los reportes
        def generar_reporte_prestamos_vencidos():
            if reporte_tipo.get() == "Tabular":
                self.mostrar_prestamos_vencidos()
            else:
                self.mostrar_prestamos_vencidos_grafico()

        def generar_reporte_libros_mas_prestados():
            if reporte_tipo.get() == "Tabular":
                self.mostrar_libros_mas_prestados()
            else:
                self.mostrar_libros_mas_prestados_grafico()

        def generar_reporte_usuarios_mas_prestamos():
            if reporte_tipo.get() == "Tabular":
                self.mostrar_usuarios_mas_prestamos()
            else:
                self.mostrar_usuarios_mas_prestamos_grafico()

        tk.Button(frame, text="Préstamos Vencidos", command=generar_reporte_prestamos_vencidos, width=30).pack(pady=10)
        tk.Button(frame, text="Libros Más Prestados Último Mes", command=generar_reporte_libros_mas_prestados, width=30).pack(pady=10)
        tk.Button(frame, text="Usuarios con Más Préstamos", command=generar_reporte_usuarios_mas_prestamos, width=30).pack(pady=10)

    def generar_pdf(self, titulo, encabezados, filas, nombre_archivo):
        # Ruta para la carpeta 'reports'
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports'))
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Ruta completa del archivo PDF
        pdf_path = os.path.join(reports_dir, nombre_archivo)
        
        # Configuración del documento con orientación horizontal
        doc = SimpleDocTemplate(pdf_path, pagesize=landscape(A4))
        
        # Estilos de documento
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title_style.textColor = colors.HexColor("#4B0082")
        title_style.fontSize = 18
        title_paragraph = Paragraph(titulo, title_style)

        # Configuración de la tabla
        col_widths = [2 * inch, 2 * inch, 2 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch]
        table_data = [encabezados] + filas
        table = Table(table_data, colWidths=col_widths)

        # Estilos de la tabla
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B0082")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray)
        ])
        table.setStyle(table_style)

        # Construcción del PDF
        elements = [title_paragraph, table]
        doc.build(elements)
        
        messagebox.showinfo("PDF Exportado", f"El reporte '{titulo}' ha sido exportado como '{nombre_archivo}' en la carpeta 'reports'.")

        # Intentar abrir el PDF automáticamente
        try:
            if os.name == 'nt':  # Windows
                os.startfile(pdf_path)
            else:  # Otros sistemas (MacOS, Linux)
                subprocess.run(["open", pdf_path])
        except Exception as e:
            messagebox.showwarning("Error al abrir PDF", f"No se pudo abrir el archivo PDF automáticamente: {e}")
    def mostrar_grafico(self, fig):
        grafico_window = tk.Toplevel(self.root)
        grafico_window.title("Visualización de Reporte")
        grafico_window.geometry("800x600")

        canvas = FigureCanvasTkAgg(fig, master=grafico_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        tk.Button(grafico_window, text="Cerrar", command=grafico_window.destroy).pack(pady=10)


    def mostrar_prestamos_vencidos(self):
        resultado = prestamo_controller.listar_prestamos_vencidos()
        if resultado:
            encabezados = ["ID", "Usuario", "Libro", "Fecha Estimada", "Fecha Real", "Días de Atraso"]
            filas = [
                [row[0], row[1], row[2], row[3], row[4], int(row[5])] for row in resultado
            ]
        else:
            encabezados = ["ID", "Usuario", "Libro", "Fecha Estimada", "Fecha Real", "Días de Atraso"]
            filas = [["Sin datos", "", "", "", "", ""]]
        
        self.generar_pdf("Préstamos Vencidos", encabezados, filas, "prestamos_vencidos.pdf")
    def mostrar_prestamos_vencidos_grafico(self):
        total_prestamos = prestamo_controller.obtener_total_prestamos()
        prestamos_vencidos = len(prestamo_controller.listar_prestamos_vencidos())
        labels = ["Préstamos Vencidos", "Préstamos a Tiempo"]
        sizes = [prestamos_vencidos, total_prestamos - prestamos_vencidos]
        colors = ['#FF6F61', '#6B8E23']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Circulo perfecto
        ax.set_title("Préstamos Vencidos")

        self.mostrar_grafico(fig)


    def mostrar_libros_mas_prestados(self):
        resultado = prestamo_controller.libros_mas_prestados_ultimo_mes()
        if resultado:
            encabezados = ["Libro", "Total Préstamos"]
            filas = [[row[0], row[1]] for row in resultado]
        else:
            encabezados = ["Libro", "Total Préstamos"]
            filas = [["Sin datos", ""]]
        self.generar_pdf("Libros Más Prestados Último Mes", encabezados, filas, "libros_mas_prestados.pdf")
    def mostrar_libros_mas_prestados_grafico(self):
        data = prestamo_controller.libros_mas_prestados_ultimo_mes()
        libros = [row[0] for row in data]
        prestamos = [row[1] for row in data]

        fig, ax = plt.subplots()
        ax.bar(libros, prestamos, color='#1E90FF')
        ax.set_xlabel("Libros")
        ax.set_ylabel("Total de Préstamos")
        ax.set_title("Libros Más Prestados Último Mes")
        ax.tick_params(axis='x', rotation=45)  # Rotar nombres de libros

        self.mostrar_grafico(fig)


    def mostrar_usuarios_mas_prestamos(self):
        resultado = prestamo_controller.usuarios_mas_prestamos()
        if resultado:
            encabezados = ["Usuario", "Total Préstamos"]
            filas = [[row[0], row[1]] for row in resultado]
        else:
            encabezados = ["Usuario", "Total Préstamos"]
            filas = [["Sin datos", ""]]
        self.generar_pdf("Usuarios con Más Préstamos", encabezados, filas, "usuarios_mas_prestamos.pdf")
    def mostrar_usuarios_mas_prestamos_grafico(self):
        data = prestamo_controller.usuarios_mas_prestamos()
        usuarios = [row[0] for row in data]
        prestamos = [row[1] for row in data]

        fig, ax = plt.subplots()
        ax.bar(usuarios, prestamos, color='#FFD700')
        ax.set_xlabel("Usuarios")
        ax.set_ylabel("Total de Préstamos")
        ax.set_title("Usuarios con Más Préstamos")
        ax.tick_params(axis='x', rotation=45)  # Rotar nombres de usuarios

        self.mostrar_grafico(fig)


if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
