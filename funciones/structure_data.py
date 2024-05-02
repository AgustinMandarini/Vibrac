# Esta funcion se encargara de abrir un archivo txt, procesarlo, reorganizarlo en diccionarios y retornar
# finalmente un diccionario de diccionarios, donde cada uno de los cuales representa una parte de datos
# del informe

from tkinter import filedialog
import matplotlib.pyplot as plt
import tkinter as tk
import io
import os

def structure_data(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        datos = file.read()
    # newDato es un array con el string original del archivo txt, donde cada linea del archivo es un elemento del array
    newDato = datos.split("\n")
    
    # Elimina las lineas vacías
    newDato = [linea for linea in newDato if linea.strip()]

    # Se elimina el primer y los dos ultimos elemento del array, ya que son caracteres que no sirven (S2 y W)
    newDato.pop(0)
    newDato = newDato[:-2]

    # En caso de que el txt venga con un string de salto de linea ('\n') ademas del salto de linea propieamente dicho, la siguiente
    # linea se encarga de eliminar el caracter sobrante 
    newDato = [linea.replace("\\n", "") for linea in newDato]

    # Se crean diccionarios y arrays para cada parte del informe (Encabezado, resultadoss, grafico1, grafico2, numSerie_fechaCalib)
    data = []
    encabezado = {"Fecha": "","Hora":"","Nombre":"","Cantidad de Muestras":"","Intervalo de muestra(s)":"", "Ponderacion":"","Integracion":"", "Analisis":""}
    resultados = {"Leq [dB]":"", "LAFMáx [dB]":"","LMáx [dB]":"", "LMín [dB]":"", "LPico [dB]":"", "L05 [dB]":"","L10 [dB]":"", "L50 [dB]":"", "L90 [dB]":"","L95 [dB]":""}
    grafico1 = []
    grafico2 = []
    
    numSerie_fechaCalib = newDato[-1].split(",") # Ultimo renglon del txt, que tiene el nro de serie y fecha de calibración

    for index, dato in enumerate(newDato):

        dato = dato.split(",")
        
        if index % 4 == 0:
            for i, (key, value) in enumerate(encabezado.items()):
                if(key == "Cantidad de Muestras" or key == "Intervalo de muestra(s)"):
                    encabezado[key] = float(dato[i])
                else:
                    encabezado[key] = dato[i]
        if index % 4 == 1:
            for i, (key, value) in enumerate(resultados.items()):
                resultados[key] = float(dato[i])/100
        if index % 4 == 2:
            for i in dato:
                grafico1.append(float(i) / 100)
        if index % 4 == 3:
            for i in dato:
                grafico2.append(float(i) / 100)
            # Agrega el bloque de medicion a la variable data
            data.append([encabezado, resultados, grafico1, grafico2])

            # Resetea los arrays y objetos para cargar un nuevo bloque en ellos
            encabezado = {"Fecha": "","Hora":"","Nombre":"","Cantidad de Muestras":"","Intervalo de muestra(s)":"", "Ponderacion":"","Integracion":"", "Analisis":""}
            resultados = {"Leq [dB]":"", "LAFMáx [dB]":"","LMáx [dB]":"", "LMín [dB]":"", "LPico [dB]":"", "L05 [dB]":"","L10 [dB]":"", "L50 [dB]":"", "L90 [dB]":"","L95 [dB]":""}
            grafico1 = []
            grafico2 = []

            # Elimina los primeros 4 indices que son los datos del primer bloque (Medicion) para que no se pise con el siguiente
            # bloque de medicon al momento de hacer append a la variable dat
            del dato[4:] 
    # Retorna un array con data (datos de las muestras) y numSerie_fechaCalib
    return [ data, numSerie_fechaCalib ]

