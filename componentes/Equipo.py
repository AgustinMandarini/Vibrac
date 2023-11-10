import tkinter as tk
import sqlite3
import ttkbootstrap as tb
from tkinter import ttk
from funciones.resource_path import resource_path
from funciones.com_descarga import com_descarga

class Equipo(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('640x480')
        self.title('Equipo')

         # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.puertos = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5']
        self.selected_puerto = tk.StringVar() # Almacena la selección del Dropdown
        
        input_frame = self.create_ui()
        input_frame.grid(column=0, row=0)

    def descargar_datos(self):
        com_descarga(self.puertos[4])
    
    def create_ui(self):

        # AQUI COMIENZA EL FORMULARIO
        frame = ttk.Frame(self)

        # Nombre del puerto
        ttk.Label(frame, text='Puerto:').grid(column=0, row=0, sticky=tk.W, pady=(10, 0))

        #Dropdown para seleccionar puerto
        self.dropdown_puerto = ttk.Combobox(frame, textvariable=self.selected_puerto, values=self.puertos)
        self.dropdown_puerto.grid(column=1, row=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Descarga de datos
        ttk.Label(frame, text='Descarga de datos:').grid(column=0, row=1, sticky=tk.W, pady=(10, 0))
        boton_descargar_datos = ttk.Button(frame, text="Descargar", command=self.descargar_datos, width= 10)
        boton_descargar_datos.grid(row=1, column=1, columnspan=2, pady=10, padx=10, ipadx=100)
        
        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame

    def error_popup(self, error):
        # Crea una ventana emergente (Toplevel)
        popup = tk.Toplevel(self)
        popup.title("Advertencia !")
        
        # Etiqueta con el mensaje de advertencia
        mensaje = tk.Label(popup, text=error)
        mensaje.pack(padx=20, pady=20)
            
        # Botón para cerrar la ventana emergente
        boton_cerrar = tk.Button(popup, text="Cerrar", command=popup.destroy)
        boton_cerrar.pack(padx=20, pady=10)