import serial
import datetime
import os
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
        response = read_until_character(ser, 'W')
 #      response = ser.read(160000)
        print(type(response.decode('utf-8')))
        print("Respuesta del dispositivo: ", response.decode('utf-8'))
#       decoded_response=response.decode('utf-8')
#       print(decoded_response[:160000])

    except serial.SerialException as e:
        print("Error de comunicacion serie: ", str(e))
    finally:
        ser.close()

    tests_path = resource_path('tests')
 #   ruta_completa = os.path.join(tests_path, f'descarga_datos_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.txt')   
    ruta_completa = os.path.join(tests_path, f'mi_archivo12.txt')   
 #   ruta_completa = 'D:\Pablo\Boreas\Python\Programas\mi_archivo9.txt'    

    # El archivo se cierra automáticamente al salir del bloque "with"
    # Abre un archivo en modo escritura ('w') para redirigir la salida
    with open(ruta_completa, 'w', encoding='utf-8') as archivo:
        # Redirige la salida de print() al archivo
     #   print("Respuesta del dispositivo:", response.decode('utf-8'), file=archivo)
        print(response.decode('utf-8'), file=archivo)
     #   print("Otra línea de salida", file=archivo)
     #   print(file=archivo)

 #   print(type(response.decode('utf-8')))

 