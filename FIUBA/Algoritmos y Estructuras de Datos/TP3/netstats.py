#!/usr/bin/python3

import sys
import grafo
import funcs_aux

PARAM_INV = ("Solo se puede pasar un argumento como parámetro")

def descomp_elems(input):
        cam = input.split()[1:]
        cam = " ".join(cam)
        el1, el2 = cam.split(",")
        return el1, el2

def main():
    args = sys.argv
    argumentos = args[1:]
    if len(argumentos) != 1:
        raise Exception(PARAM_INV)
    wiki = argumentos[0]
    grafo_wiki = grafo.Grafo(True)
    articulos = {}
    funcs_aux.crear_grafo_art(wiki, grafo_wiki, articulos)

    for input in sys.stdin:
        comando = input.split()[0]
        if comando == "listar_operaciones":
            funcs_aux.listar_operaciones()
        if comando == "camino":
            origen, destino = descomp_elems(input)
            funcs_aux.camino(grafo_wiki, origen, destino, articulos)
        if comando == "rango":
            articulo, rango = descomp_elems(input)
            funcs_aux.todos_en_rango(grafo_wiki, articulo, rango, articulos)
        if comando == "diametro":
            funcs_aux.diametro(grafo_wiki)
        if comando == "navegacion":
            origen = input.split()[1:]
            origen = " ".join(origen)
            funcs_aux.navegacion_primer_link(grafo_wiki, origen, articulos)
        if comando == "clustering":
            origen = None
            if len (input.split()) > 1:
                origen = input.split()[1:]
                origen = " ".join(origen)
            funcs_aux.clustering(grafo_wiki, origen, articulos)
        if comando == "lectura":
            lista = input.split()[1:]
            lista = " ".join(lista)
            lista = lista.split(",")
            funcs_aux.lectura_2am(grafo_wiki, lista, articulos)
        

main()