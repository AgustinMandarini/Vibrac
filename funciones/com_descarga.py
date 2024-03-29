import serial
import datetime
import os
from funciones.resource_path import resource_path

def com_descarga(puerto):

    ser = serial.Serial(
        port=puerto,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1
    )

    #data = ser.read(10)
    try:
        connect = 'T'
        ser.write(connect.encode())

        response = ser.read(100)

        print("Respuesta del dispositivo: ", response.decode('utf-8'))
    except serial.SerialException as e:
        print("Error de comunicacion serie: ")
    finally:
        ser.close()
        # Abre un archivo en modo escritura ('w')
    tests_path = resource_path('tests')
    ruta_completa = os.path.join(tests_path, f'descarga_datos_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.txt')   

    # El archivo se cierra automáticamente al salir del bloque "with"
    # Abre un archivo en modo escritura ('w') para redirigir la salida
    with open(ruta_completa, 'w', encoding='utf-8') as archivo:
        # Redirige la salida de print() al archivo
        print("Respuesta del dispositivo:", response.decode('utf-8'), file=archivo)
        print("Otra línea de salida", file=archivo)