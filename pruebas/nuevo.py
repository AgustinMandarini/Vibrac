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
    
    valores = []
    for linea in lineas:
        valor = float(linea.strip())  # Leer solo el valor numérico
        valores.append(valor)
    
    n = len(valores)
    etiquetas = list(range(1, n+1))  # Crear etiquetas del 1 al n
    
    plt.bar(etiquetas, valores, color='skyblue')
    plt.xlabel('Frecuencias(Hz)')
    plt.ylabel('Ruido(DB)')
    plt.title('Leq vs 1/3 de Octava')
    plt.ylim(50, 130)  # Rango en el eje y
    plt.tight_layout()

    plt.show()

# Crear la ventana
ventana = tk.Tk()
ventana.title("Generador de Gráfico de Barras Personalizado")

# Crear un botón para abrir el cuadro de diálogo de selección de archivo
boton_abrir = tk.Button(ventana, text="Seleccionar Archivo", command=abrir_archivo)
boton_abrir.pack(pady=20)

ventana.mainloop()