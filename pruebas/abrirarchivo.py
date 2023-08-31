#Esto lo que hace es a partir de un archivo txt que tenga una cantidad n de dos valores separados por una coma crear un gráfico de barras. 
#Antes de ejecutarlo tenés que instalar:
#    pip install matplotlib


import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Función para abrir el cuadro de diálogo de selección de archivo
def abrir_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt")])
    if ruta_archivo:
        generar_grafico(ruta_archivo)

# Función para generar el gráfico de barras
def generar_grafico(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    
    etiquetas = []
    valores = []
    for linea in lineas:
        etiqueta, valor = linea.strip().split(',')
        etiquetas.append(etiqueta)
        valores.append(float(valor))
    
    plt.bar(etiquetas, valores, color='skyblue')
    plt.xlabel('Categorías')
    plt.ylabel('Valores')
    plt.title('Gráfico de Barras Personalizado')
    plt.ylim(0, 10)  # Rango en el eje y
    plt.tight_layout()

    plt.show()

# Crear la ventana
ventana = tk.Tk()
ventana.title("Generador de Gráfico de Barras Personalizado")

# Crear un botón para abrir el cuadro de diálogo de selección de archivo
boton_abrir = tk.Button(ventana, text="Seleccionar Archivo", command=abrir_archivo)
boton_abrir.pack(pady=20)

ventana.mainloop()