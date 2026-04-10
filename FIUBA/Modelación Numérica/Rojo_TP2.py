
"""
CALCULADORA DE SDI (Streamflow Drought Index) A PARTIR DE UN ARCHIVO CSV
Testeado con la estación 16 - río San Francisco, Caimancito, Jujuy, Argentina.

Se espera recibir un archivo csv con un encabezado, y el resto de sus lineas con formato:
dd/mm/aaaa h:mm;ccc,cc 
donde los valores asociados a c representan el Caudal Medio Mensual, en m³/s
EJ: 01/01/1947 0:00;217

Si algún año hidrológico está incompleto, se saltea, sus datos no son tomados en cuenta, y se avisa por pantalla.
Esto es así porque el Sistema Nacional de Información Hídrica tampoco calcula valores como Caudal Específico o Máximo Medio Diario para años incompletos.
Si hay un año hidrológico entero faltante en el intervalo de años evaluados, ni siquiera se avisa por pantalla.

Para usarlo, ejecutar el archivo python por consola, junto a la ruta del archivo csv que se desea analizar.
Adicionalmente, se pueden ver los datos de un año concreto si se le pasa como segundo parámetro un año hidrológico presente en el archivo!
Se espera que el segundo parámetro sea un string de la forma aaaa/bbbb, siendo A y B años consecutivos.
EJ de comandos ejecución (probé en Ubuntu nada más, asumo que la sintaxis es la misma en Windows):
>python3 Rojo_TP2.py ruta/Estacion_16.csv
>python3 Rojo_TP2.py ruta/Estacion_16.csv 2022/2023
Notar que aunque se pida los datos de un año específico, el análisis de dicho año va a utilizar los datos de todos los años disponibles del archivo csv para el calculo de la media y la desviación.

Actualmente se asume que el año hidrológico va de Septiembre a Agosto. Si no es el caso, cambiar constante global MESES_H a tu orden específico de meses. Tambien cambiar PRIMER_MES y ULTIMO_MES.
Tener en cuenta que si el año hidrológico es igual a un año natural (es decir, va de enero a diciembre), va a haber que ajustar algunas cosas en formateo_lineas,
Ya que se asume que un año hidrológico tiene componentes de dos años naturales distintos consecutivos.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Modelación numérica - Rojo Santiago - 110700
"""

import numpy as np

import sys

PRIMER_MES, ULTIMO_MES = "Septiembre", "Agosto"

INTERVALOS = {"k1": 3, "k2": 6, "k3": 9, "k4": 12}

MESES_H = ["09", "10", "11", "12", "01", "02", "03", "04", "05", "06", "07", "08"]

CLASIFICACION_SEQUIA = [
    (float('-inf'), -2.0, "Sequía Extrema"),
    (-2.0, -1.5, "Sequía Severa"),
    (-1.5, -1.0, "Sequía Moderada"),
    (-1.0, 0.0, "Sequía Suave"),
    (0.0, float('inf'), "Sin Sequía")
]

#Función de lectura. Preferí hacer mi propia funcion de lectura para poder formatear el archivo mas cómodamente
def leer_archivo(archivo):
    caudales = {}
    try:
        with open (archivo) as f:
            f.readline() #Saltea el encabezado del csv
            for linea in f.readlines():
                if linea.rstrip(): #Saltea lineas vacias
                    formateo_lineas(caudales, linea)
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}")
        return {}
    except Exception as e:
        print(f"Error leyendo el archivo {archivo}. Error: {e}")
        return {}
    return caudales

#formatea cada linea a medida que se lee del archivo csv
def formateo_lineas(caudales, linea):

    # Estandariza cada linea, reemplaza cada separador por uno en comun (" ") y separa en dia, mes, año, hora y caudal. También reemplaza la coma del caudal por un punto, para luego poder transformarlo a float
    formateo = (linea.rstrip().translate(str.maketrans({"/": " ", ";": " ", ",": "."}))).split()
    formateo.pop(3)  # La hora no nos interesa
    formateo.pop(0)  # El dia tampoco interesa
    mes, anio, caudal = formateo[0], formateo[1], float(formateo[2])

    if int(mes) <= int(MESES_H[-1]): #Por ahora, int(MESES_H[-1]) = 8, pero escalabilidad y coso
        aux_anio = int(anio) - 1
        clave = str(aux_anio) + "/" + anio
    else:
        aux_anio = int(anio) + 1
        clave = anio + "/" + str(aux_anio)

    caudales[clave] = caudales.get(clave, {})
    caudales[clave][mes] = caudal  # diccionario de diccionarios que separa en año hidrológico. Dentro de cada año se puede acceder al caudal de cada mes. EJ: {'1947/1948': {'09': 16.87, '10': 12.29, ...}...}

#Calcula el volumen anual por intervalos. Solo toma años que estén completos
def calcular_vol_anual(caudales):
    resultados = {}
    caudales_ordenados = []
    for mes in MESES_H:
        if mes in caudales:
            caudales_ordenados.append(caudales[mes]) #Busca los caudales de los meses ordenados segun orden cronológico de mes hidrológico
        else:
            return None #Si el año esta incompleto se descarta.

    for inter_k, mes_k in INTERVALOS.items():
        resultados[inter_k] = round(sum(caudales_ordenados[:mes_k]), 2)
    return resultados

#Calcula la media y la desviación de todos los años procesados
def calcular_media_desviacion_historica(volumenes_totales):
    medias, desviaciones, volumen_intervalo  = {}, {}, {}
    for k in INTERVALOS.keys():
        volumen_intervalo[k] = []

    for anio, volumenes_anio in volumenes_totales.items():
        for k, volumen in volumenes_anio.items():
            volumen_intervalo[k].append(volumen)  #Queda un diccionario con los 4 intervalos, cada uno con una lista de los valores anuales del respectivo intervalo. EJ: {'k1': [41.59, 25.55, ...], 'k2': [...], ...}

    for k in INTERVALOS.keys():
        medias[k] = round(float(np.mean(volumen_intervalo[k])), 2)
        desviaciones[k] = round(float(np.std(volumen_intervalo[k])), 2)
    return medias, desviaciones

#La función principal de la lógica del programa.
def calcular_sdi(archivo):
    caudales = leer_archivo(archivo)

    if not caudales: #Error leyendo el archivo
        return {}

    print(f"Datos cargados para {len(caudales)} años hidrológicos")
    volumenes_totales = {}
    for anio, caudales_anio in caudales.items():
        volumenes = calcular_vol_anual(caudales_anio)
        if volumenes is not None:
            volumenes_totales[anio] = volumenes
        else:
            print (f"año {anio} incompleto. Salteando...")

    medias, desviaciones = calcular_media_desviacion_historica(volumenes_totales)

    resultados = {}
    for anio, volumenes_anio in volumenes_totales.items():
        resultados[anio] = {}
        for k in INTERVALOS.keys():
            sdi = round((volumenes_anio[k] - medias[k]) / desviaciones[k], 2)
            tipo = clasificar_sequia(sdi)
            resultados[anio][k] = {"SDI": round(sdi, 2), "Volumen acumulado": round(volumenes_anio[k], 2), "Tipo": tipo}
    return resultados

def clasificar_sequia(sdi):
    for limite_inf, limite_sup, tipo in CLASIFICACION_SEQUIA:
        if limite_inf <= sdi < limite_sup:
            return tipo

#Función encargada de imprimir los datos. También se puede imprimir datos de un año especifico! Para eso pasarle el año hidrológico deseado en formato "aaaa/bbbb" como 2do parámetro
def mostrar_resultados(resultados, anio_especifico=None):
    if not resultados:
        print("No hay resultados para mostrar!")
        return

    if anio_especifico:
        if anio_especifico not in resultados:
            print(f"No hay datos disponibles para {anio_especifico}")
            return
        print(f"\n === RESULTADOS SDI PARA AÑO HIDROLÓGICO {anio_especifico}")
        print(f" === MESES DEL AÑO HIDROLÓGICO: {PRIMER_MES} - {ULTIMO_MES}")
        mostrar_anio(resultados[anio_especifico], anio_especifico)
    else:
        print(f"\n === RESULTADOS SDI PARA TODOS LOS AÑOS DISPONIBLES")
        print(f" === MESES DEL AÑO HIDROLÓGICO: {PRIMER_MES} - {ULTIMO_MES}")
        print(f" === PERÍODO ANALIZADO: {min(resultados.keys())} a {max(resultados.keys())}")
        print(f" === TOTAL DE AÑOS ANALIZADOS: {len(resultados)}")
        for anio in sorted(resultados.keys()):
            mostrar_anio(resultados[anio], anio)

def mostrar_anio(datos, anio):
    print("-" * 60)
    print(f"Año hidrológico: {anio}")
    print("-" * 60)
    for k in INTERVALOS.keys():
        info = datos[k]
        meses = INTERVALOS[k]
        print(f"||{k} ({meses} meses)||")
        print(f"SDI = {info["SDI"]}")
        print(f"Volumen = {info["Volumen acumulado"]} m³/s")
        print(f"Tipo de sequía: {info["Tipo"]} \n")

def main():
    if len(sys.argv) == 1:
        print("Se debe recibir un archivo!")
        return
    archivo, anio = sys.argv[1], None
    if len(sys.argv) == 3:
        anio = sys.argv[2]
    res = calcular_sdi(archivo)
    mostrar_resultados(res, anio)

if __name__ == "__main__":
    main()