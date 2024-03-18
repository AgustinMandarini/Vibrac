import os
import PyPDF2
import subprocess
from jinja2 import Environment, FileSystemLoader
import pdfkit
from funciones.structure_data import structure_data
import matplotlib.pyplot as plt
import numpy as np
import datetime
import base64
from funciones.resource_path import resource_path

def generar_informe(ruta_archivo, mediciones, empresa, instrumento, nro_informe, titulo, empleado, fecha, observaciones):
    # importa la funcion structure_data y retorna los dos grupos de datos
    # data contiene toda la informacion de cada una de las muestras
    # numSerie_fechaCalib contiene un array con el nro de serie y fecha de calibración
    data, numSerie_fechaCalib = structure_data(ruta_archivo)
    ##### CREAR PAGINA 1 DEL INFORME A PARTIR DE UN TEMPLATE HTML #####

     # Utiliza la funcion resource_path para traer el path tanto si la aplicacion corre en distribucion o en desarrollo
    template_path = resource_path('template')
    
    # Crear un entorno Jinja2
    env = Environment(loader=FileSystemLoader(template_path))

    # Cargar el template HTML
    template = env.get_template('pagina_1_template.html')
    
    html_content = template.render(
        data=data,
        empresa=empresa,
        instrumento=instrumento,
        nro_informe=nro_informe, 
        titulo=titulo, 
        empleado=empleado, 
        fecha=fecha,
        observaciones=observaciones,
        numSerie_fechaCalib=numSerie_fechaCalib,
        mediciones=mediciones
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

        if muestra[0]["Nombre"] in mediciones:
            # Datos para el grafico 1
            intervalo = muestra[0]["Intervalo de muestra(s)"] / 60
            cantidad_muestras = muestra[0]["Cantidad de Muestras"]

            # Obtener valores para el eje x
            x1 = np.arange(0.0, cantidad_muestras, intervalo) # Crea tambien intervalos de tiempo
            x2 = ["63", "80", "100", "125", "160", "200", "250", "315", "400", "500", "630", "800", "1 k", "1,25 k", "1,6 k", "2 k", "2,5 k", "3,15 k", "4 k", "5 k", "6,3 k", "8 k", "10 k", "12,5 k", "16 k", "20 k"]
            
            # Obtener valores para eje y
            y1 = muestra[2]
            y2 = muestra[3]

            # Crear los 2 gráficos, y define el tamaño de la figura
            fig, (ax1, ax2)  = plt.subplots(2, figsize=(10,8))

            # Ajusta los margenes izquierdo y derecho
            plt.subplots_adjust(left=0.05, right=0.99, hspace=0.6)

            # Crea el ploy con los valores x, y entregados
            ax1.plot(x1, y1)
            # ax2.bar(x2, y2, width=1, edgecolor="white", linewidth=0.7)

            ax1.set(xlabel='Tiempo (min)', ylabel='Ruido [dB]',
                title='Ruido vs Tiempo')
            ax1.grid() # establece un grid de fondo para el primer grafico
            ax2.set(xlabel='Frecuencia [Hz]', ylabel='Ruido [dB]',
                title='Leq vs 1/3 de Octava')
            
            # Rotar las etiquetas del eje x en 45 grados
            ax2.set_xticklabels(x2, rotation= -45, ha="center")
            
            ax2.grid(zorder=1) # zorder define un orden de aparicion menor que las barras
            ax2.bar(x2, y2, zorder=2) #zorder define un orden de aparicion mayor que la grid

            # Renderizar el template con los datos
            img_path = os.path.join(template_path, 'grafico1.png')
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

    # Abrir el PDF con el visor de PDF predeterminado del sistema
    try:
        process = subprocess.Popen(['start', pdf_path], shell=True)
        process.wait()  # Espera a que el visor de PDF se cierre antes de continuar
    except FileNotFoundError:
        # Si no se encuentra el visor de PDF predeterminado, abrir el PDF con Chrome
        try:
            subprocess.Popen(['chrome', pdf_path], shell=True)
        except FileNotFoundError:
            # Si no se encuentra Chrome, abrir el PDF con el navegador predeterminado
            subprocess.Popen(['start', pdf_path], shell=True)