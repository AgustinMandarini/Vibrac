import tkinter as tk
from tkinter import ttk, filedialog
from funciones.ver_medicion import ver_medicion
from funciones.structure_data import structure_data

class Mediciones(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('640x640')
        self.title('Mediciones')

         # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        # Guardara la ruta del archivo de descargas de datos. Será buscado por la funcion abrir_archivo la cual
        # lo guardara en esta variable. Luego la funcion imprimir_informe lo utilizara para imprimir el informe
        self.ruta_archivo = None
                
        self.empresas = [] # Guardara los nombres de todas las empresas
        self.selected_empresa = tk.StringVar() # Almacena la selección del Dropdown

        self.instrumentos = [] # Guardara los nombres de todas los instrumentos
        self.selected_instrumento = tk.StringVar() # Almacena la selección del Dropdown  

        self.mediciones_seleccionadas = [] # Guarda los nombres de las mediciones correspondientes a la descarga seleccionada

        input_frame = self.create_main_mediciones_window()
        input_frame.grid(column=0, row=0)

    # Crea un frame para la ventana mediciones
    def create_main_mediciones_window(self):

        # Crea un frame sobre donde armar el formulario
        frame = ttk.Frame(self)

        # Boton de seleccion de archivo
        boton_abrir_archivo = ttk.Button(frame, text='Seleccione archivo de descarga', command=self.abrir_archivo)
        boton_abrir_archivo.grid(row=1, column=0, columnspan=1, pady=0, padx=0, ipadx=10)

        # Listbox para mostrar las mediciones
        ttk.Label(frame, text='Seleccione las mediciones:').grid(row=2, column=0, sticky=tk.W)
        self.listbox = tk.Listbox(frame, height=6, selectmode=tk.EXTENDED)
        self.listbox.grid(row=1, column=1, columnspan=2, pady=10, padx=10, ipadx=100)
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

         # link a scrollbar to a list
        scrollbar = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        self.listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=1, column=2, sticky='ns')

        # Boton para mostrar mediciones
        boton_ver_medicion = ttk.Button(frame, text="Ver medición", command=self.ver_medicion, width= 10)
        boton_ver_medicion.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame

    def mostrar_popup(self, error):
        # Crea una ventana emergente (Toplevel)
        popup = tk.Toplevel(self)
        popup.title("Advertencia !")
        
        # Etiqueta con el mensaje de advertencia
        mensaje = tk.Label(popup, text=error)
        mensaje.pack(padx=20, pady=20)
        
        # Botón para cerrar la ventana emergente
        boton_cerrar = tk.Button(popup, text="Cerrar", command=popup.destroy)
        boton_cerrar.pack(padx=20, pady=10)

    def cargar_mediciones(self):
        try:
            self.listbox.delete(0, tk.END)
            data, numSerie_fechaCalib = structure_data(self.ruta_archivo)
            for i, muestra in enumerate(data):
                nombre_muestra = muestra[0]["Nombre"]
                self.listbox.insert(tk.END, nombre_muestra)

        except Exception as e:
            self.mostrar_popup(e)

    def abrir_archivo(self):
        try:
            self.ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt")])
            self.cargar_mediciones()
        except Exception as e:
            self.mostrar_popup(e)

    def items_selected(self, event):
        indices = self.listbox.curselection()
        self.mediciones_seleccionadas = [self.listbox.get(i) for i in indices]

    # Muestra los graficos de las mediciones
    def ver_medicion(self):

        if not self.ruta_archivo:
            self.mostrar_popup("Debe seleccionar un archivo")
        else:
            try:
                # Llama a la funcion importada "ver_medicion"
                ver_medicion(self.ruta_archivo, self.mediciones_seleccionadas)
            except Exception as e:
                print(e)
                self.mostrar_popup(e)