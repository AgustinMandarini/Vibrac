import os
import PyPDF2
from jinja2 import Environment, FileSystemLoader
import pdfkit
from funciones.structure_data import structure_data
import matplotlib.pyplot as plt
import numpy as np
import datetime
import webbrowser
import base64

def generar_informe(ruta_archivo, empresa, nro_informe, titulo, empleado, fecha):
    # importa la funcion structure_data y retorna los dos grupos de datos
    # data contiene toda la informacion de cada una de las muestras
    # numSerie_fechaCalib contiene un array con el nro de serie y fecha de calibración
    data, numSerie_fechaCalib = structure_data(ruta_archivo)
    ##### CREAR PAGINA 1 DEL INFORME A PARTIR DE UN TEMPLATE HTML #####

    # Obtener la ruta del directorio donde se encuentra el script actual
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al directorio de templates
    template_directory = os.path.join(script_directory, '..', 'template')

    # Crear un entorno Jinja2
    env = Environment(loader=FileSystemLoader(template_directory))

    # Cargar el template HTML
    template = env.get_template('pagina_1_template.html')
    
    html_content = template.render(
        data=data,
        empresa=empresa,
        nro_informe=nro_informe, 
        titulo=titulo, 
        empleado=empleado, 
        fecha=fecha,
        numSerie_fechaCalib=numSerie_fechaCalib,
        )
    # Configuracion del path para wkhtmltopdf
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    pdf_path = f'informe_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    pdfkit.from_string(html_content, pdf_path, configuration=config)

    ##### CREAR RESTO DEL INFORME #####

    # Crear un objeto PDF para el archivo final
    pdf_writer = PyPDF2.PdfWriter()

    # Agregar la página 1 al PDF final
    pdf_writer.add_page(PyPDF2.PdfReader(pdf_path).pages[0])

    # Crea un nuevo entorno de jinja para el nuevo template
    template = env.get_template('paginas_restantes_template.html')

    # Itera sobre data, que es un array donde cada uno de sus elementos son los datos correspondientes a cada medicion
    for i, muestra in enumerate(data):

        # Datos para el grafico 1
        intervalo = muestra[0]["Intervalo de muestra(s)"] / 60
        cantidad_muestras = muestra[0]["Cantidad de Muestras"]

        # Obtener valores para el eje x
        x1 = np.arange(0.0, cantidad_muestras, intervalo) # Crea tambien intervalos de tiempo
        # x2 = [63, 80, 100, 125]
        
        # Obtener valores para eje y
        y1 = muestra[2]
        # y2 = muestra[3]

        # Crear los 2 gráficos, y define el tamaño de la figura
        fig, (ax1, ax2)  = plt.subplots(2, figsize=(10,4))

        # Ajusta los margenes izquierdo y derecho
        plt.subplots_adjust(left=0.05, right=0.99)

        # Crea el ploy con los valores x, y entregados
        ax1.plot(x1, y1)
        # ax2.bar(x2, y2, width=1, edgecolor="white", linewidth=0.7)

        ax1.set(xlabel='Tiempo (min)', ylabel='Ruido [dB]',
            title='Ruido vs Tiempo')
        ax1.grid()
        ax2.set(xlabel='Frecuencia [Hz]', ylabel='Ruido [dB]',
            title='Leq vs 1/3 de Octava') # FALTA HACER QUE DIGA DINAMICAMENTE PARA CUANDO ES 1 OCTAVA O 1/3 DE OCTAVA
        ax2.grid()

        # Renderizar el template con los datos
        img_path = os.path.join(template_directory, 'grafico1.png')
        plt.savefig(img_path)

        # Convertir la imagen en base64 para que pdfkit pueda leerla y transformarla en pdf
        with open(img_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')


        temp_html_content = template.render(
            data=muestra, 
            numSerie_fechaCalib=numSerie_fechaCalib, 
            img_base64 = img_base64)

        temp_pdf_path = f"temp_informe_muestra_{i+1}.pdf"

        pdfkit.from_string(temp_html_content, temp_pdf_path, configuration=config)
        pdf_reader = PyPDF2.PdfReader(temp_pdf_path)
        pdf_writer.add_page(pdf_reader.pages[0])
        

        os.remove(temp_pdf_path)
        os.remove(img_path)

    # Guardar el PDF final
    with open(pdf_path, "wb") as final_pdf_file:
        pdf_writer.write(final_pdf_file)

    # webbrowser.open(pdf_path)