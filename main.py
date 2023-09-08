import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk
from componentes.Reportes import Reportes
from componentes.Empresas import Empresas
from componentes.Instrumentos import Instrumentos

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        window_width = 800
        window_height = 600

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Crea un estilo de ttkbootstrap
        self.style = tb.Style(theme='flatly')
        
        # Aplica las configuraciones globales a todos los widgets ttk
        self.style.configure('.', font=("Calibri", 10))

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
                    command=lambda t=text: self.open_window(t)).grid(row=1, column=index, columnspan=1, pady=50, padx=30, ipadx=10)
                

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
    app.mainloop()