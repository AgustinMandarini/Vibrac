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

        # Lista de empresas (inicialmente vacía)
        self.empresas = []
        
        input_frame = self.create_ui()
        input_frame.grid(column=0, row=0)


        # Empresa seleccionada en el listbox
        self.empresa_seleccionada = None

    # Busca las empresas anteriormente utilizadas
    def ver_empresas(self):
        conn = sqlite3.connect('Reportes_vibraciones_db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM empresas")
        empresas = c.fetchall()
        
        # Itera sobre los resultados de la consulta a la base de datos
        empresas_nuevas = [str(empresa[0]) for empresa in empresas]
            # Agregar las empresas recuperadas de la base de datos a la lista existente
        self.empresas.extend(empresas_nuevas)
        self.actualizar_lista_empresas()

        def items_selected(event):
            # Obtener la empresa seleccionada
            indice = self.listbox.curselection()
            self.empresa_seleccionada = self.listbox.get(indice)

        self.listbox.bind('<<ListboxSelect>>', items_selected)
        
        conn.commit()
        conn.close()
    
    def create_ui(self):
        # Crea un frame para la ventana empresas
        def borrar_datos_db():
            conn = sqlite3.connect('Reportes_vibraciones_db')
            c = conn.cursor()
            conn.commit()
            try:
                c.execute("DELETE from empresas WHERE nombre = ?", (self.empresa_seleccionada,))
                conn.commit()
                # Borra la empresa de la lista de empresas
                self.empresas.remove(self.empresa_seleccionada)
                self.actualizar_lista_empresas()
            except Exception as e:
                print(e)
                self.error_popup(e)
            finally:
                conn.close()

        # Agrega los datos ingresados a la base de datos. Se ejecuta al clickear el boton "agregar"
        def agrergar_datos_db():
            conn = sqlite3.connect('Reportes_vibraciones_db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO empresas VALUES (:nombre, :direccion, :localidad, :provincia)", 
                        {
                            'nombre': nombre.get(), 
                            'direccion': direccion.get(),
                            'localidad': localidad.get(),
                            'provincia': provincia.get()
                        })

                conn.commit()
                # Agrega la empresa a la lista de empresas
                self.empresas.append(nombre.get())
                self.actualizar_lista_empresas()
            except Exception as e:
                print(e)
                self.error_popup(e)
            finally:
                conn.close()

            # limpiar los datos ingresados
            nombre.delete(0, tk.END)
            direccion.delete(0, tk.END)
            localidad.delete(0, tk.END)
            provincia.delete(0, tk.END)


        def actualizar_popup():
            # Funcion encargada de actualizar la base de datos
            def actualizar_datos_db():
                conn = sqlite3.connect('Reportes_vibraciones_db')
                c = conn.cursor()
                try:
                    c.execute(f"UPDATE empresas SET nombre = :nombre, direccion = :direccion, localidad = :localidad, provincia = :provincia WHERE nombre = :empresa_seleccionada",
                            {
                                'nombre': nombre.get(),
                                'direccion': direccion.get(),
                                'localidad': localidad.get(),
                                'provincia': provincia.get(),
                                'empresa_seleccionada': self.empresa_seleccionada
                            })

                    conn.commit()
                    # Actualiza la listbox con el nuevo cambio realizado
                    index = self.empresas.index(self.empresa_seleccionada)
                    self.empresas[index] = nombre.get()
                    self.actualizar_lista_empresas()

                except Exception as e:
                    print(e)
                    self.error_popup(e)
                finally:
                    conn.close()
            # Crea una ventana emergente (Toplevel)
            popup = tk.Toplevel(self)
            popup.title("Actualizar informacion de empresa")
            
            # Nombre de la empresa
            ttk.Label(popup, text='Nombre:').grid(column=0, row=0, sticky=tk.W, pady=(10, 0))
            nombre = ttk.Entry(popup, width=30)
            nombre.focus()
            nombre.grid(column=1, row=0, sticky=tk.W, pady=(10, 0))

            # Direccion de la empresa:
            ttk.Label(popup, text='Direccion:').grid(column=0, row=1, sticky=tk.W)
            direccion = ttk.Entry(popup, width=30)
            direccion.grid(column=1, row=1, sticky=tk.W)

            # Localidad de la empresa:
            ttk.Label(popup, text='Localidad:').grid(column=0, row=2, sticky=tk.W)
            localidad = ttk.Entry(popup, width=30)
            localidad.grid(column=1, row=2, sticky=tk.W)

            # Provincia de la empresa:
            ttk.Label(popup, text='Provincia:').grid(column=0, row=3, sticky=tk.W)
            provincia = ttk.Entry(popup, width=30)
            provincia.grid(column=1, row=3, sticky=tk.W)

            # Boton de agregar
            boton_agregar = ttk.Button(popup, text="Actualizar", command=actualizar_datos_db, width= 10)
            boton_agregar.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # AQUI COMIENZA EL FORMULARIO
        frame = ttk.Frame(self)

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
        boton_agregar.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

         # Listbox para mostrar las empresas
        self.listbox = tk.Listbox(frame, height=6, selectmode=tk.SINGLE)
        self.listbox.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        # link a scrollbar to a list
        scrollbar = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        self.listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=5, column=2, sticky='ns')

        # Vincular la selección del Listbox a la variable empresa_seleccionada
        self.listbox.bind('<<ListboxSelect>>', lambda event: self.seleccionar_empresa(event))

        # Boton borrar registro en base de datos
        boton_borrar_registro = ttk.Button(frame, text="Borrar", command=borrar_datos_db, width=2)
        boton_borrar_registro.grid(row=6, column=0, columnspan=1, pady=10, padx=10, ipadx=100)

        # Boton actualizar registro en base de datos
        boton_actualizar_registro = ttk.Button(frame, text="Actualizar", command=actualizar_popup, width=2)
        boton_actualizar_registro.grid(row=6, column=1, columnspan=1, pady=10, padx=10, ipadx=100)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        # Ejecuta el listbox con las empresas
        self.ver_empresas()

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

    def actualizar_lista_empresas(self):
        # Actualiza la lista de empresas en el Listbox
        self.listbox.delete(0, tk.END)  # Borra todos los elementos actuales
        for empresa in self.empresas:
            self.listbox.insert(tk.END, empresa)