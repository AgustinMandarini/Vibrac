import os
import serial
import datetime
import tkinter as tk
from tkinter import filedialog
from funciones.resource_path import resource_path

def read_until_character(ser, end_char):
    result = bytearray()
    while True:
        byte = ser.read(1)
        if not byte:
            continue  # Si no hay datos, seguir esperando
        result.append(byte[0])
        if byte.decode('utf-8') == end_char:
            break
    return bytes(result)

# Lee datos hasta encontrar el carácter 'W'

def com_descarga(puerto):

    ser = serial.Serial(
        port=puerto,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=50
    )

    try:
        connect = 'T'
        ser.write(connect.encode())
        #response = read_until_character(ser, 'W')
        response = ser.read(160000)
        print(type(response.decode('utf-8')))
        print("Respuesta del dispositivo: ", response.decode('utf-8'))
#       decoded_response=response.decode('utf-8')
#       print(decoded_response[:160000])

    except serial.SerialException as e:
        print("Error de comunicacion serie: ", str(e))
    finally:
        ser.close()

   # tests_path = resource_path('tests')
   # ruta_completa = os.path.join(tests_path, f'descarga_datos_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.txt')   
    # ruta_completa = os.path.join(tests_path, f'mi_archivo12.txt')   
  # ruta_completa = 'D:\Pablo\Boreas\Python\Programas\mi_archivo9.txt'    
 #   print(type(response.decode('utf-8')))

def save_as_text_file(response):
    ruta_completa = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if ruta_completa:
        try:
            # El archivo se cierra automáticamente al salir del bloque "with"
            # Abre un archivo en modo escritura ('w') para redirigir la salida
            with open(ruta_completa, 'w', encoding='utf-8') as archivo:
                # Redirige la salida de print() al archivo
            #   print("Respuesta del dispositivo:", response.decode('utf-8'), file=archivo)
                archivo.write(response.decode('utf-8'))
            #   print("Otra línea de salida", file=archivo)
            #   print(file=archivo)
                tk.messagebox.showinfo("Éxito!",  "Archivo de descarga creado exitosamente!")
        except Exception as e:
            mostrar_popup(e)

def mostrar_popup(error):
        # Crea una ventana emergente (Toplevel)
        popup = tk.Toplevel()
        popup.title("Error al crear archivo de descarga")
        
        # Etiqueta con el mensaje de advertencia
        mensaje = tk.Label(popup, text=error)
        mensaje.pack(padx=20, pady=20)
        
        # Botón para cerrar la ventana emergente
        boton_cerrar = tk.Button(popup, text="Cerrar", command=popup.destroy)
        boton_cerrar.pack(padx=20, pady=10)