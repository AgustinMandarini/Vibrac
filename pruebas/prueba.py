datos = """S2\n
26/02/2023,21:35:29,Medicion01,5,60,A,L,3\n
6612,8080,7874,4106,9903,7366,7135,6015,5166,5083\n
6360,6736,7070,5972,4858\n
5841,6581,6941,6431,6314,5743,6265,5617,5500,6011,5994,5489,6231,6070,5674,5443,5697,5068,4946,4530,4096,3565,3279,3144,3108,3056\n
26/02/2023,21:42:38,Medicion02,5,60,A,L,3\n
6972,8411,8128,4159,10339,7771,7525,6403,5461,5230\n
6691,6244,7010,7442,6371\n
6228,6181,6690,6552,6426,6355,6977,6676,6235,6462,6762,5959,6383,6297,5840,5821,5778,5124,4985,4677,4468,3809,3474,3362,3118,3057\n
45633,11/07/22\n
W"""

# newDato es un array con el string original del archivo txt, donde cada linea del archivo es un elemento del array
newDato = datos.split("\n\n")
# Se elimina el primer y ultimo elemento del array, ya que son caracteres que no sirven (S2 y W)
newDato.pop(0)
newDato.pop(-1)
print(newDato)

# Se crean diccionarios y arrays para cada parte del informe (Encabezado, resultadoss, grafico1, grafico2, numSerie_fechaCalib)

encabezado = {"Fecha": "","Hora":"","Nombre":"","Cantidad de Muestras":"","Intervalo de muestra (s)":"", "Ponderacion":"","Integracion":"", "Analisis":""}
resultados = {"Leq [dB]":"", "LAFMáx [dB]":"","LMáx [dB]":"", "LMín [dB]":"", "LPico [dB]":"", "L05 [dB]":"","L10 [dB]":"", "L50 [dB]":"", "L90 [dB]":"","L95 [dB]":""}
grafico1 = []
grafico2 = []
numSerie_fechaCalibnumSerie_fechaCalib = newDato[-1].split(",")

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
    