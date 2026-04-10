import random
from typing import List, Tuple, Any
import niveles
import unruly
Grilla = Any

def formar_grilla(grilla: Grilla):
    """Recibe la grilla y la imprime en la terminal de manera agradable para el usuario.
    Incluye contadores de filas y de columnas"""
    conteo_de_columnas = "  |"
    for i in range (len(grilla[0])):
        conteo_de_columnas += (str(i)+" |")
    
    copia_grilla = grilla.copy()
    remplazo_vacio = "".join(copia_grilla)
    resultado_remplazo = remplazo_vacio.replace(" ", "_")
    lista_de_remplazo = []
    for i in range (0, len(resultado_remplazo), len(grilla[0])):
        lista_de_remplazo.append(resultado_remplazo[i:i+len(grilla[0])])

    reemplazar_espacios = []
    for i in range (len(lista_de_remplazo)):
        reemplazar_espacios.append((lista_de_remplazo[i].replace("","  "))[2:-1])

    print (conteo_de_columnas)
    for i in range (len(grilla)):
        print (str(i) + "| " + reemplazar_espacios[i])

def main():
    nivel = random.choice(niveles.NIVELES)
    grilla = unruly.crear_grilla(nivel)
    dimensiones = unruly.dimensiones(grilla)
    while unruly.grilla_terminada(grilla) == False:
        formar_grilla(grilla)  
        while True:
            print ("Entrada: [valor,columna,fila] \nPara salir: o")
            entrada = input("Entrada: ")
            coordenadas = entrada.split(",")
            if len(coordenadas) == 3:
                if coordenadas[1].isdigit() and coordenadas[2].isdigit():
                    if coordenadas[0] == " " or coordenadas[0] == "0" or coordenadas[0] == "1":
                        if int(coordenadas[1]) < int(dimensiones[0]) and int(coordenadas[2]) < int(dimensiones[1]):
                            break
            else:
                if entrada == "o":
                    return None
        if coordenadas[0] == "1":
            grilla = unruly.cambiar_a_uno(grilla, int(coordenadas[1]), int(coordenadas[2]))
        if coordenadas[0] == "0":
            grilla = unruly.cambiar_a_cero(grilla, int(coordenadas[1]), int(coordenadas[2]))
        if coordenadas[0] == " ":
            grilla = unruly.cambiar_a_vacio(grilla, int(coordenadas[1]), int(coordenadas[2]))
    formar_grilla(grilla)
    print ("sos una genio")

main()