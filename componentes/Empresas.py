import tkinter as tk
import sqlite3
from tkinter import ttk

class Empresas(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('640x480')
        self.title('Empresas')

        ttk.Button(self,
                text='Close',
                command=self.destroy).grid(row=1, column=1, padx=10, pady=10)

         # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        input_frame = self.create_main_empresas_window()
        input_frame.grid(column=0, row=0)

    def create_main_empresas_window(self):
        # Busca las empresas anteriormente utilizadas
        def ver_empresas():
            conn = sqlite3.connect('Reportes_vibraciones_db')
            c = conn.cursor()

            c.execute("SELECT *, oid FROM empresas")
            empresas = c.fetchall()
            
            # Itera sobre los resultados de la consulta a la base de datos
            imprimir_empresas = ""
            
            for empresa in empresas:
                imprimir_empresas += str(empresa[0])+'\n'
            
            variable = tk.Variable(value=imprimir_empresas)
            listbox = tk.Listbox(frame, listvariable=variable, height=6, selectmode=tk.SINGLE) 
            listbox.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
            
            conn.commit()
            conn.close()
            
        # Crea un frame para la ventana empresas
        def borrar_datos_db():
            conn = sqlite3.connect('Reportes_vibraciones_db')
            c = conn.cursor()

            c.execute("DELETE from empresas WHERE oid = " + box_borrar_registro.get())

            conn.commit()
            conn.close()

        # Agrega los datos ingresados a la base de datos. Se ejecuta al clickear el boton "agregar"
        def agrergar_datos_db():
            conn = sqlite3.connect('Reportes_vibraciones_db')
            c = conn.cursor()

            c.execute("INSERT INTO empresas VALUES (:nombre, :direccion, :localidad, :provincia)", 
                    {
                        'nombre': nombre.get(), 
                        'direccion': direccion.get(),
                        'localidad': localidad.get(),
                        'provincia': provincia.get()
                    })

            conn.commit()
            conn.close()

            # limpiar los datos ingresados
            nombre.delete(0, tk.END)
            direccion.delete(0, tk.END)
            localidad.delete(0, tk.END)
            provincia.delete(0, tk.END)

        frame = ttk.Frame(self)

        # Ejecuta el listbox con las empresas
        ver_empresas()

        # Nombre de la empresa
        ttk.Label(frame, text='Nombre:').grid(column=0, row=0, sticky=tk.W, pady=(10, 0))
        nombre = ttk.Entry(frame, width=30)
        nombre.focus()
        nombre.grid(column=1, row=0, sticky=tk.W, pady=(10, 0))

        # Direccion de la empresa:
        ttk.Label(frame, text='Direccion:').grid(column=0, row=1, sticky=tk.W)
        direccion = ttk.Entry(frame, width=30)
        direccion.grid(column=1, row=1, sticky=tk.W)

        # Localidad de la empresa:
        ttk.Label(frame, text='Localidad:').grid(column=0, row=2, sticky=tk.W)
        localidad = ttk.Entry(frame, width=30)
        localidad.grid(column=1, row=2, sticky=tk.W)

        # Provincia de la empresa:
        ttk.Label(frame, text='Provincia:').grid(column=0, row=3, sticky=tk.W)
        provincia = ttk.Entry(frame, width=30)
        provincia.grid(column=1, row=3, sticky=tk.W)

        # Boton de agregar
        boton_agregar = ttk.Button(frame, text="Agregar", command=agrergar_datos_db, width= 10)
        boton_agregar.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Borrar registro en base de datos
        box_borrar_registro = ttk.Entry(frame, width=30)
        box_borrar_registro.grid(row=10, column=1, pady=5)
        label_borrar_registro = ttk.Label(frame, text="Borrar ID: ")
        label_borrar_registro.grid(row=10, column=0, pady=5)
        boton_borrar_registro = ttk.Button(frame, text="Borrar empresa", command=borrar_datos_db, width= 10)
        boton_borrar_registro.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame