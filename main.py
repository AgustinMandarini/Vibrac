import tkinter as tk
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

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # main window title
        self.title('VIBRACIONES')
        
        buttons_labels = ['Equipo', 'Empresas', 'Instrumentos', 'Mediciones', 'Reportes']
        # place a button on the root window for every string in buttons_labels
        for text in buttons_labels:
            ttk.Button(self,
                    text=text,
                    command=lambda t=text: self.open_window(t)).pack(expand=True)
                

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