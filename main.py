import tkinter as tk
import ttkbootstrap as tb
import time
from PIL import Image, ImageTk
from tkinter import ttk
from componentes.Reportes import Reportes
from componentes.Empresas import Empresas
from componentes.Instrumentos import Instrumentos

class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.overrideredirect(True)  # Elimina los bordes y título de la ventana
        window_width = 400
        window_height = 300

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Crear un lienzo (canvas) para mostrar la imagen
        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack()

        # Cargar y redimensionar la imagen
        original_image = Image.open("./img/instrutech_TRIAX.jpeg")

        # Obtener el ancho y alto de la imagen original
        original_width, original_height = original_image.size

        # Calcular la nueva altura manteniendo las proporciones originales
        new_height = int((window_width / original_width) * original_height)
        
        resized_image = original_image.resize((window_width, new_height), Image.LANCZOS)

        # Convertir la imagen redimensionada a PhotoImage
        self.photo = ImageTk.PhotoImage(resized_image)

        # Centrar la imagen en el lienzo
        x = (window_width - resized_image.width) / 2
        y = (window_height - resized_image.height) / 2

         # Mostrar la imagen en el lienzo
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo)

        ## required to make window show before the program gets to the mainloop
        self.update()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        splash = Splash(self)

        window_width = 744
        window_height = 600

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Crea un estilo de ttkbootstrap
        self.style = tb.Style(theme='flatly')
        
        # Aplica las configuraciones globales a todos los widgets ttk
        self.style.configure('.', font=("Calibri", 12))

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # main window title
        self.title('VIBRACIONES')
        
        buttons_labels = ['Equipo', 'Empresas', 'Instrumentos', 'Mediciones', 'Reportes']

        # Botones principales ubicados horizontalmente
        for index, text in enumerate(buttons_labels):
            tb.Button(self,
                    text=text,
                    command=lambda t=text: self.open_window(t)).grid(row=1, column=index, columnspan=1, pady=50, padx=20, ipadx=10)

        ## simulate a delay while loading
        time.sleep(3)

        ## show window again
        self.deiconify()

        ## finished loading so destroy splash
        splash.destroy()

    def open_window(self, text):
        if text == 'Reportes':
            window = Reportes(self)
            window.grab_set()
        if text == 'Empresas':
            window = Empresas(self)
            window.grab_set()
        if text == 'Instrumentos':
            window = Instrumentos(self)
            window.grab_set()

if __name__ == "__main__":
    app = App()
    app.resizable(False, False)
    app.mainloop()