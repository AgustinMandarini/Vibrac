import os
import shutil
from funciones.resource_path import resource_path

def eliminar_archivos_temporales():

    pdf_location = resource_path('temp')
    # Eliminar todos los archivos en el directorio
    for archivo in os.listdir(pdf_location):
        ruta_archivo = os.path.join(pdf_location, archivo)
        try:
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
            elif os.path.isdir(ruta_archivo):
                shutil.rmtree(ruta_archivo)
        except Exception as e:
            print(f"No se pudo eliminar {ruta_archivo}: {e}")