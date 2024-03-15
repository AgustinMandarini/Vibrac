import tkinter as tk
import sqlite3
import datetime
from tkinter import ttk, filedialog, Text
from funciones.generar_informe import generar_informe, structure_data
from funciones.resource_path import resource_path

class Reportes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Utiliza la funcion resource_path para traer el path tanto si la aplicacion corre en distribucion o en desarrollo
        self.db_path = resource_path('db\\Reportes_vibraciones_db')

        self.geometry('640x640')
        self.title('Reportes')

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

        # Ejecuta la funcion ver_empresas al momento de iniciar el componente
        self.ver_empresas()

        # Ejecuta la funcion ver_instrumentos al momento de iniciar el componente
        self.ver_instrumentos()

        input_frame = self.create_main_reportes_window()
        input_frame.grid(column=0, row=0)

    # Crea un frame para la ventana reportes
    def create_main_reportes_window(self):

        # Crea un frame sobre donde armar el formulario
        frame = ttk.Frame(self)

        # Numero de informe
        ttk.Label(frame, text='Numero de informe:').grid(column=0, row=0, sticky=tk.W, pady=(10, 0))
        self.nro_informe = ttk.Entry(frame, width=30)
        self.nro_informe.focus()
        self.nro_informe.grid(column=1, row=0, sticky=tk.W, pady=(10, 0))

        # Titulo del informe
        ttk.Label(frame, text='Titulo:').grid(column=0, row=1, sticky=tk.W)
        self.titulo = ttk.Entry(frame, width=30)
        self.titulo.grid(column=1, row=1, sticky=tk.W)

        # Empleado que genera el informe
        ttk.Label(frame, text='Empleado:').grid(column=0, row=2, sticky=tk.W)
        self.empleado = ttk.Entry(frame, width=30)
        self.empleado.grid(column=1, row=2, sticky=tk.W)

        # Fecha del informe
        self.fecha = datetime.datetime.now().strftime('%d-%m-%Y')
        ttk.Label(frame, text=f'Fecha: {self.fecha}').grid(column=0, row=3, sticky=tk.W)

        # Boton de seleccion de archivo
        boton_abrir_archivo = ttk.Button(frame, text='Seleccione archivo de descarga', command=self.abrir_archivo)
        boton_abrir_archivo.grid(row=4, column=0, columnspan=1, pady=0, padx=0, ipadx=10)

        # Dropdown de empresas
        ttk.Label(frame, text='Empresa:').grid(column=0, row=5, sticky=tk.W)
        self.dropdown_empresas = ttk.Combobox(frame, textvariable=self.selected_empresa, values=self.empresas)
        self.dropdown_empresas.grid(row=5, column=1, columnspan=2, pady=10, padx=10, ipadx=100)

        # Dropdown de instrumentos
        ttk.Label(frame, text='Instrumento:').grid(column=0, row=6, sticky=tk.W)
        self.dropdown_instrumentos = ttk.Combobox(frame, textvariable=self.selected_instrumento, values=self.instrumentos)
        self.dropdown_instrumentos.grid(row=6, column=1, columnspan=2, pady=10, padx=10, ipadx=100)

        # Textarea de observaciones
        ttk.Label(frame, text='Observaciones:').grid(column=0, row=7, sticky=tk.W)
        self.observaciones = Text(frame, height=5, width=20)
        self.observaciones.grid(row=7, column=1, columnspan=2, pady=10, padx=10, ipadx=100)

        # Listbox para mostrar las mediciones
        ttk.Label(frame, text='Seleccione las mediciones:').grid(column=0, row=8, sticky=tk.W)
        self.listbox = tk.Listbox(frame, height=6, selectmode=tk.EXTENDED)
        self.listbox.grid(row=8, column=1, columnspan=2, pady=10, padx=10, ipadx=100)
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

         # link a scrollbar to a list
        scrollbar = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        self.listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=8, column=2, sticky='ns')

        # Boton para imprimir informe
        boton_imprimir_informe = ttk.Button(frame, text="Imprimir Informe", command=self.imprimir_informe, width= 10)
        boton_imprimir_informe.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


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

    # Imprimira el informe y tambien creara un registro en la tabla informes
    def imprimir_informe(self):

        if not self.ruta_archivo:
            self.mostrar_popup("Debe seleccionar un archivo")
        elif not self.selected_empresa.get():
            self.mostrar_popup("Debe seleccionar una empresa")
        elif not self.selected_instrumento:
            self.mostrar_popup("Debe seleccionar un instrumento")
        else:
            try:
                # Accede a las variables de los Entry
                nro_informe = self.nro_informe.get()
                titulo = self.titulo.get()
                empleado = self.empleado.get()
                fecha = self.fecha
                observaciones = self.observaciones.get("1.0", "end")
                
                # Llama a la funcion importada "generar_informe"
                generar_informe(
                    self.ruta_archivo, 
                    self.mediciones_seleccionadas,
                    self.selected_empresa.get(),
                    self.selected_instrumento.get(), 
                    nro_informe, 
                    titulo, 
                    empleado, 
                    fecha,
                    observaciones)
            except Exception as e:
                print(e)
                self.mostrar_popup(e)

    # Busca las empresas anteriormente agregadas
    def ver_empresas(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute("SELECT *, oid FROM empresas")
        empresas = c.fetchall()
        
        # Itera sobre los resultados de la consulta a la base de datos y agrega los nombres de las empresas a la variable
        self.empresas = [empresa[0] for empresa in empresas]
                                
        conn.commit()
        conn.close()

    # Busca los instrumentos anteriormente agregados
    def ver_instrumentos(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute("SELECT *, oid FROM instrumentos")
        instrumentos = c.fetchall()
        
        # Itera sobre los resultados de la consulta a la base de datos y agrega los nombres de las empresas a la variable
        self.instrumentos = [instrumento[1] for instrumento in instrumentos]
                                
        conn.commit()
        conn.close()

    