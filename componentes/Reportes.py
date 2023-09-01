import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import filedialog
from funciones.generar_informe import generar_informe
import datetime

class Reportes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('640x480')
        self.title('Reportes')

         # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        # Guardara la ruta del archivo de descargas de datos. Será buscado por la funcion abrir_archivo la cual
        # lo guardara en esta variable. Luego la funcion imprimir_informe lo utilizara para imprimir el informe
        self.ruta_archivo = None
                
        self.empresas = [] # Guardara los nombres de todas las empresas
        self.selected_empresa = tk.StringVar() # Almacena la selección del Dropdown  

        # Ejecuta la funcion ver_empresas al momento de iniciar el componente
        self.ver_empresas()

        input_frame = self.create_main_reportes_window()
        input_frame.grid(column=0, row=0)

    # Crea un frame para la ventana reportes
    def create_main_reportes_window(self):
        
        # def borrar_datos_db():
        #     conn = sqlite3.connect('Reportes_vibraciones')
        #     c = conn.cursor()

        #     c.execute("DELETE from empresas WHERE oid = " + box_borrar_registro.get())

        #     conn.commit()
        #     conn.close()

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

        # Dropdown de empresas
        ttk.Label(frame, text='Empresa:').grid(column=0, row=4, sticky=tk.W)
        self.dropdown_empresas = ttk.Combobox(frame, textvariable=self.selected_empresa, values=self.empresas)
        self.dropdown_empresas.grid(row=4, column=1, columnspan=2, pady=10, padx=10, ipadx=100)
        # box_borrar_registro = ttk.Entry(frame, width=30)
        # box_borrar_registro.grid(row=10, column=1, pady=5)
        # label_borrar_registro = ttk.Label(frame, text="Borrar ID: ")
        # label_borrar_registro.grid(row=10, column=0, pady=5)
        # boton_borrar_registro = ttk.Button(frame, text="Borrar empresa", command=borrar_datos_db, width= 10)
        # boton_borrar_registro.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Boton de seleccion de archivo
        boton_abrir_archivo = ttk.Button(frame, text='Buscar archivo', command=self.abrir_archivo)
        boton_abrir_archivo.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Boton para imprimir informe
        boton_imprimir_informe = ttk.Button(frame, text="Imprimir Informe", command=self.imprimir_informe, width= 10)
        boton_imprimir_informe.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Boton para imprimir informe
        boton_mostrar_informes = ttk.Button(frame, text="Ver informes emitidos", command=None, width= 10)
        boton_mostrar_informes.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

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

    def abrir_archivo(self):
        try:
            self.ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt")])
        except Exception as e:
            self.mostrar_popup(e)

    # Imprimira el informe y tambien creara un registro en la tabla informes
    def imprimir_informe(self):
        
            if not self.ruta_archivo:
                self.mostrar_popup("Debe seleccionar un archivo")
            elif not self.selected_empresa.get():
                self.mostrar_popup("Debe seleccionar una empresa")
            else:
                try:
                    # Accede a las variables de los Entry
                    nro_informe = self.nro_informe.get()
                    titulo = self.titulo.get()
                    empleado = self.empleado.get()
                    fecha = self.fecha
                    
                    # Llama a la funcion importada "generar_informe"
                    generar_informe(
                        self.ruta_archivo, 
                        self.selected_empresa.get(), 
                        nro_informe, 
                        titulo, 
                        empleado, 
                        fecha)
                except Exception as e:
                    print(e)
                    self.mostrar_popup(e)

    # Busca las empresas anteriormente utilizadas
    def ver_empresas(self):
        conn = sqlite3.connect('Reportes_vibraciones')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM empresas")
        empresas = c.fetchall()
        
        # Itera sobre los resultados de la consulta a la base de datos y agrega los nombres de las empresas a la variable
        self.empresas = [empresa[0] for empresa in empresas]
                                
        conn.commit()
        conn.close()

    # Agrega los datos ingresados a la tabla informes
    def agrergar_datos_db():
        conn = sqlite3.connect('Reportes_vibraciones')
        c = conn.cursor()

        c.execute("SELECT oid FROM empresas WHERE oid=" + self.selected_empresa.get())
        empresa_oid = c.fetchone()
    
        try:
            c.execute("INSERT INTO informes VALUES (:nro_informe, :empleado, :fecha, :id_empresa, id_instrumento, archivo_descarga)", 
                    {
                        'nro_informe': nro_informe.get(), 
                        'titulo': titulo.get(),
                        'empleado': empleado.get(),
                        'fecha': fecha.get(),
                        'id_empresa': empresa_oid,
                        # 'id_instrumento': id_instrumento.get(),
                        'archivo_descarga': archivo_descarga.get()
                    })
        except Exception as e:
            print(f"Error al crear registro en informes: {e}")

        conn.commit()
        conn.close()

        # limpiar los datos ingresados
        nro_informe.delete(0, tk.END)
        empleado.delete(0, tk.END)
        fecha.delete(0, tk.END)
        id_empresa.delete(0, tk.END)
        id_instrumento.delete(0, tk.END)
        archivo_descarga.delete(0, tk.END)