import tkinter as tk
import sqlite3
from tkinter import ttk

class Instrumentos(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('640x480')
        self.title('Instrumentos')

         # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        # Lista de instrumentos (inicialmente vacía)
        self.instrumentos = []
        
        input_frame = self.create_ui()
        input_frame.grid(column=0, row=0)


        # Instrumento seleccionado en el listbox
        self.modelo_instrumento_seleccionado = None

    # Busca las instrumentos anteriormente utilizadas
    def ver_instrumentos(self):
        conn = sqlite3.connect('./db/Reportes_vibraciones_db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM instrumentos")
        instrumentos = c.fetchall()
        
        # Itera sobre los resultados de la consulta a la base de datos
        # instrumento[1] corresponde al modelo
        instrumentos_nuevos = [str(instrumento[1]) for instrumento in instrumentos]
        # Agregar los instrumentos recuperados de la base de datos a la lista existente
        self.instrumentos.extend(instrumentos_nuevos)
        self.actualizar_lista_instrumentos()

        def items_selected(event):
            # Obtener el instrumento seleccionado
            indice = self.listbox.curselection()
            self.modelo_instrumento_seleccionado = self.listbox.get(indice)

        self.listbox.bind('<<ListboxSelect>>', items_selected)
        
        conn.commit()
        conn.close()
    
    def create_ui(self):
        # Crea un frame para la ventana instrumentos
        def borrar_datos_db():
            conn = sqlite3.connect('./db/Reportes_vibraciones_db')
            c = conn.cursor()
            conn.commit()
            try:
                c.execute("DELETE from instrumentos WHERE modelo = ?", (self.modelo_instrumento_seleccionado,))
                conn.commit()
                # Borra el instrumento de la lista de instrumentos
                self.instrumentos.remove(self.modelo_instrumento_seleccionado)
                self.actualizar_lista_instrumentos()
            except Exception as e:
                print(e)
                self.error_popup(e)
            finally:
                conn.close()

        # Agrega los datos ingresados a la base de datos. Se ejecuta al clickear el boton "agregar"
        def agregar_datos_db():
            conn = sqlite3.connect('./db/Reportes_vibraciones_db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO instrumentos VALUES (:marca, :modelo, :nro_serie, :fecha, :certificado_nro)", 
                        {
                            'marca': marca.get(), 
                            'modelo': modelo.get(),
                            'nro_serie': nro_serie.get(),
                            'fecha': fecha.get(),
                            'certificado_nro': certificado_nro.get(),
                        })

                conn.commit()
                # Agrega la empresa a la lista de instrumentos
                self.instrumentos.append(marca.get())
                self.actualizar_lista_instrumentos()
            except Exception as e:
                print(e)
                self.error_popup(e)
            finally:
                conn.close()

            # limpiar los datos ingresados
            marca.delete(0, tk.END)
            modelo.delete(0, tk.END)
            nro_serie.delete(0, tk.END)
            fecha.delete(0, tk.END)
            certificado_nro.delete(0, tk.END)


        def actualizar_popup():
            # Funcion encargada de actualizar la base de datos
            def actualizar_datos_db():
                conn = sqlite3.connect('./db/Reportes_vibraciones_db')
                c = conn.cursor()
                try:
                    c.execute(f"UPDATE instrumentos SET marca = :marca, modelo = :modelo, nro_serie = :nro_serie, fecha = :fecha, certificado_nro = :certificado_nro WHERE modelo = :modelo_instrumento_seleccionado",
                            {
                                'marca': marca.get(),
                                'modelo': modelo.get(),
                                'nro_serie': nro_serie.get(),
                                'fecha': fecha.get(),
                                'certificado_nro': certificado_nro.get(),
                                'modelo_instrumento_seleccionado': self.modelo_instrumento_seleccionado
                            })

                    conn.commit()
                    # Actualiza la listbox con el nuevo cambio realizado
                    index = self.instrumentos.index(self.modelo_instrumento_seleccionado)
                    self.instrumentos[index] = modelo.get()
                    self.actualizar_lista_instrumentos()

                except Exception as e:
                    print(e)
                    self.error_popup(e)
                finally:
                    conn.close()

            # Obtener los datos del registro seleccionado desde la base de datos
            conn = sqlite3.connect('./db/Reportes_vibraciones_db')
            c = conn.cursor()
            c.execute("SELECT * FROM instrumentos WHERE modelo = ?", (self.modelo_instrumento_seleccionado,))
            registro = c.fetchone()  # Debería haber solo un registro con el mismo modelo
            print(self.modelo_instrumento_seleccionado)
            print(registro)

            # Crea una ventana emergente (Toplevel)
            popup = tk.Toplevel(self)
            popup.title("Actualizar informacion de instrumento")
            
            # Marca del instrumento
            ttk.Label(popup, text='Marca:').grid(column=0, row=0, sticky=tk.W, pady=(10, 0))
            marca = ttk.Entry(popup, width=30)
            marca.insert(0, registro[0])
            marca.grid(column=1, row=0, sticky=tk.W, pady=(10, 0))

            # Modelo del instrumento:
            ttk.Label(popup, text='Modelo:').grid(column=0, row=1, sticky=tk.W)
            modelo = ttk.Entry(popup, width=30)
            modelo.insert(0, registro[1])
            modelo.grid(column=1, row=1, sticky=tk.W)

            # nro_serie del instrumento:
            ttk.Label(popup, text=' nro_serie:').grid(column=0, row=2, sticky=tk.W)
            nro_serie = ttk.Entry(popup, width=30)
            nro_serie.insert(0, registro[2])
            nro_serie.grid(column=1, row=2, sticky=tk.W)

            # Fecha del instrumento:
            ttk.Label(popup, text='Fecha:').grid(column=0, row=3, sticky=tk.W)
            fecha = ttk.Entry(popup, width=30)
            fecha.insert(0, registro[3])
            fecha.grid(column=1, row=3, sticky=tk.W)

            # Nro Certificado del instrumento:
            ttk.Label(popup, text='Nro Certificado:').grid(column=0, row=3, sticky=tk.W)
            certificado_nro = ttk.Entry(popup, width=30)
            certificado_nro.insert(0, registro[4])
            certificado_nro.grid(column=1, row=3, sticky=tk.W)

            # Boton de actualizar
            boton_actualizar = ttk.Button(popup, text="Actualizar", command=actualizar_datos_db, width= 10)
            boton_actualizar.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # AQUI COMIENZA EL FORMULARIO
        frame = ttk.Frame(self)

        # Marca del instrumento
        ttk.Label(frame, text='Marca:').grid(column=0, row=0, sticky=tk.W, pady=(10, 0))
        marca = ttk.Entry(frame, width=30)
        marca.focus()
        marca.grid(column=1, row=0, sticky=tk.W, pady=(10, 0))

        # Modelo del instrumento:
        ttk.Label(frame, text='Modelo:').grid(column=0, row=1, sticky=tk.W)
        modelo = ttk.Entry(frame, width=30)
        modelo.grid(column=1, row=1, sticky=tk.W)

        # nro_serie del instrumento:
        ttk.Label(frame, text='Nro. Serie:').grid(column=0, row=2, sticky=tk.W)
        nro_serie = ttk.Entry(frame, width=30)
        nro_serie.grid(column=1, row=2, sticky=tk.W)

        # Fecha del instrumento:
        ttk.Label(frame, text='Fecha:').grid(column=0, row=3, sticky=tk.W)
        fecha = ttk.Entry(frame, width=30)
        fecha.grid(column=1, row=3, sticky=tk.W)

        # certificado_nro del instrumento:
        ttk.Label(frame, text='Nro. Certificado:').grid(column=0, row=4, sticky=tk.W)
        certificado_nro = ttk.Entry(frame, width=30)
        certificado_nro.grid(column=1, row=4, sticky=tk.W)

        # Boton de agregar
        boton_agregar = ttk.Button(frame, text="Agregar", command=agregar_datos_db, width= 10)
        boton_agregar.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Listbox para mostrar los instrumentos
        self.listbox = tk.Listbox(frame, height=6, selectmode=tk.SINGLE)
        self.listbox.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        # link a scrollbar to a list
        scrollbar = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        self.listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=6, column=2, sticky='ns')

        # Vincular la selección del Listbox a la variable modelo_instrumento_seleccionado
        self.listbox.bind('<<ListboxSelect>>', lambda event: self.seleccionar_instrumento(event))

        # Boton borrar registro en base de datos
        boton_borrar_registro = ttk.Button(frame, text="Borrar", command=borrar_datos_db, width=2)
        boton_borrar_registro.grid(row=7, column=0, columnspan=1, pady=10, padx=10, ipadx=100)

        # Boton actualizar registro en base de datos
        boton_actualizar_registro = ttk.Button(frame, text="Actualizar", command=actualizar_popup, width=2)
        boton_actualizar_registro.grid(row=7, column=1, columnspan=1, pady=10, padx=10, ipadx=100)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        # Ejecuta el listbox con los instrumentos
        self.ver_instrumentos()

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

    def actualizar_lista_instrumentos(self):
        # Actualiza la lista de instrumentos en el Listbox
        self.listbox.delete(0, tk.END)  # Borra todos los elementos actuales
        for empresa in self.instrumentos:
            self.listbox.insert(tk.END, empresa)