import tkinter as tk
from gui.bibliotecaGUI import BibliotecaApp  # Import the GUI class

def main():
    # Create the main application window
    root = tk.Tk()
    app = BibliotecaApp(root)  # Initialize the BibliotecaApp GUI
    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    main()
