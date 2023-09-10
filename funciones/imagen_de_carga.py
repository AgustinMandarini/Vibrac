import tkinter as tk
from PIL import Image, ImageTk

def imagen_de_carga():
    # Crear una ventana de Tkinter sin bordes ni título
    ventana = tk.Tk()
    ventana.overrideredirect(True)  # Elimina los bordes y título de la ventana
    ventana.geometry("300x200")  # Ajusta el tamaño de la ventana según tus necesidades

    # Cargar y mostrar una imagen en la ventana
    #imagen = Image.open("./img/instrutech_TRIAX.jpeg")
    #imagen = ImageTk.PhotoImage(imagen)
    #label_imagen = tk.Label(ventana, image=imagen)
    label_imagen = tk.Label(ventana, text="PUTA VIRGEN PUTA PUTA ABORTADA HUJA DE PUTA")
    label_imagen.grid(column=0, row=0)

    return ventana
