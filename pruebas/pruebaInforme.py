from tkinter import filedialog
from fpdf import FPDF
import matplotlib.pyplot as plt
import tkinter as tk
import io
import os

# Función para abrir el cuadro de diálogo de selección de archivo
def abrir_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt")])
    if ruta_archivo:
        generar_informe(ruta_archivo)
def generar_informe(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        datos = file.read()
    # newDato es un array con el string original del archivo txt, donde cada linea del archivo es un elemento del array
    newDato = datos.split("\n")

    # Se elimina el primer y los dos ultimos elemento del array, ya que son caracteres que no sirven (S2 y W)
    newDato.pop(0)
    newDato = newDato[:-2]

    # En caso de que el txt venga con un string de salto de linea ('\n') ademas del salto de linea propieamente dicho, la siguiente
    # linea se encarga de eliminar el caracter sobrante 
    newDato = [linea.replace("\\n", "") for linea in newDato]

    # Se crean diccionarios y arrays para cada parte del informe (Encabezado, resultadoss, grafico1, grafico2, numSerie_fechaCalib)
    encabezado = {"Fecha": "","Hora":"","Nombre":"","Cantidad de Muestras":"","Intervalo de muestra(s)":"", "Ponderacion":"","Integracion":"", "Analisis":""}
    resultados = {"Leq [dB]":"", "LAFMáx [dB]":"","LMáx [dB]":"", "LMín [dB]":"", "LPico [dB]":"", "L05 [dB]":"","L10 [dB]":"", "L50 [dB]":"", "L90 [dB]":"","L95 [dB]":""}
    grafico1 = []
    grafico2 = []
    numSerie_fechaCalib = newDato[-1].split(",")

    for index, dato in enumerate(newDato):
        dato = dato.split(",")
        if index == 0:
            for i, (key, value) in enumerate(encabezado.items()):
                encabezado[key] = dato[i]
        if index == 1:
            for i, (key, value) in enumerate(resultados.items()):
                resultados[key] = dato[i]
        if index == 2:
            for i in dato:
                grafico1.append(i)
        if index == 3:
            for i in dato:
                grafico2.append(i)
    data = {
        "encabezado": encabezado, 
        "resultados": resultados, 
        "grafico1": grafico1, 
        "grafico2" : grafico1, 
        "numSerie_fechaCalib" : numSerie_fechaCalib
        }
    # Retorna un diccionario de diccionarios, cada uno de ellos una parte del informe
    return data

# Crear la ventana
ventana = tk.Tk()
ventana.title("Generador de Gráfico de Barras Personalizado")

# Crear un botón para abrir el cuadro de diálogo de selección de archivo
boton_abrir = tk.Button(ventana, text="Seleccionar Archivo", command=abrir_archivo)
boton_abrir.pack(pady=20)

ventana.mainloop()