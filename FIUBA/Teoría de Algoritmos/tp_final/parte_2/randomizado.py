#NO SE UTILIZA
from grafoRandomizado import Grafo
import random


def agregar_inversores(grafo: Grafo, inversores: dict):
    for i in inversores.keys():
        grafo.agregar_vertice(i,inversores[i])

# Esta funcion hace una eliminacion de la lista pisando el valor del elemento a eliminar
# con el ultimo elemento de la lista. Luego hace pop al ultimo elemento. Actualizando las posiciones
# de los elementos que se almacenan en el diccionario
def eliminacion_O_1(inversoresLista:list, inversores:dict, inversor):
    ultimoElemento = len(inversoresLista)-1
    inversoresLista[inversores[inversor]] = inversoresLista[ultimoElemento]
    inversores[inversoresLista[ultimoElemento]] = inversores[inversor] 
    inversoresLista.pop()
    inversores.pop(inversor)
    return inversoresLista

def quitar_vecinos_e_inversor(grafo: Grafo, inversores: dict, inversoresLista, inversor, vecinos:dict):
    eliminados = {}
    eliminados[inversor] = grafo.obtener_valor(inversor)
    inversoresLista = eliminacion_O_1(inversoresLista, inversores, inversor)
    for inversor in vecinos:
        eliminados[inversor] = grafo.obtener_valor(inversor)
        inversoresLista = eliminacion_O_1(inversoresLista, inversores, inversor)
    return eliminados

def agregar_vecinos_e_inversor(inversores:dict , inversoresLista:list ,eliminados: dict,):
    for inversor in eliminados.keys():
        inversores[inversor] = len(inversoresLista)
        inversoresLista.append(inversor)
    return 0

def inversores_lista(inversores:dict):
    lista = []
    posicion = 0
    for inversor in inversores.keys():
        lista.append(inversor)
        inversores[inversor] = posicion
        posicion +=1
    return lista

def insercion_aleatoria(nuevoGrafo: Grafo, grafo:Grafo, inversores:dict, inversoresLista):
    if not inversoresLista:
        return [nuevoGrafo.valor_grafo(), nuevoGrafo.obtener_vertices()]
    
    eleccionAleatoria = random.choice(inversoresLista)
    nuevoGrafo.agregar_vertice(eleccionAleatoria, grafo.obtener_valor(eleccionAleatoria))
    vecindades = grafo.eliminar_vecindades(eleccionAleatoria)
    eliminados = quitar_vecinos_e_inversor(grafo, inversores, inversoresLista ,eleccionAleatoria, vecindades)
    resultado_actual = insercion_aleatoria(nuevoGrafo, grafo, inversores, inversoresLista)
    nuevoGrafo.eliminar_vertice_sin_vecinos(eleccionAleatoria)
    agregar_vecinos_e_inversor(inversores, inversoresLista ,eliminados)
    grafo.agregar_vecindades(vecindades)

    return resultado_actual

def completar_desde_grafo_vacio(grafo: Grafo):
    if grafo.obtener_aristas() == 0:
        return grafo.valor_grafo()
    nuevoGrafo = Grafo()
    inversoresSinEnemigos = grafo.vertices_sin_vecinos()
    agregar_inversores(nuevoGrafo, inversoresSinEnemigos)
    inversoresConEnemigos:dict = grafo.vertices_con_vecinos()
    if not inversoresConEnemigos:
        return nuevoGrafo.valor_grafo()
    inversoresconEnemigosLista:list = inversores_lista(inversoresConEnemigos)

    inicios = list(inversoresConEnemigos.keys())
    resultado = [0,{}]

    for inversor in inicios:
        nuevoGrafo.agregar_vertice(inversor, grafo.obtener_valor(inversor))
        vecindades = grafo.eliminar_vecindades(inversor)
        eliminados = quitar_vecinos_e_inversor(grafo, inversoresConEnemigos, inversoresconEnemigosLista ,inversor, vecindades)
        resultado_actual = insercion_aleatoria(nuevoGrafo, grafo, inversoresConEnemigos, inversoresconEnemigosLista)
        if resultado_actual[0] > resultado[0]:
            resultado = resultado_actual
        nuevoGrafo.eliminar_vertice_sin_vecinos(inversor)
        agregar_vecinos_e_inversor(inversoresConEnemigos, inversoresconEnemigosLista ,eliminados)
        grafo.agregar_vecindades(vecindades)

    return [resultado[0], resultado[1]]


def busqueda_aleatoria(grafo: Grafo):     
    if grafo.aristas == 0:
        return [grafo.valor_grafo()]
    # if(grafo.obtener_aristas()> grafo.cantidad_vertices()):
    return completar_desde_grafo_vacio(grafo)

def main():
    # creo el grafo
    print(f"Ejemplo 1: {ejemplo_1()}. Óptimo: (['B', 'C'], 2100.0)")
    print(f"Ejemplo 2: {ejemplo_2()}. Óptimo: (['A', 'C', 'E'], 275.0)")
    print(f"Ejemplo 3: {ejemplo_3()}. Óptimo: (['A'], 1000000.0)")

    return 0

def generar_busqueda_aleatoria(inversores: list, dinero:list, conflictos:dict):
    grafo = Grafo()
    i = 0
    for inversor in inversores:
        grafo.agregar_vertice(inversor, dinero[i])
        i+=1
    
    grafo.agregar_vecindades(conflictos)

    return busqueda_aleatoria(grafo)

def ejemplo_1():
    inversores = ["A", "B", "C"]
    dinero = [2000.0, 1100.0, 1000.0]
    conflictos = {"A": {"B":{}, "C":{}}}
    return generar_busqueda_aleatoria(inversores, dinero, conflictos)

def ejemplo_2():
        inversores = ["A", "B", "C", "D", "E"]
        dinero = [100.0, 90.0, 95.0, 85.0, 80.0]
        conflictos = {"A": {"B":{}}, "B": {"C":{}}, "C": {"D":{}}, "D": {"E":{}}}
        return generar_busqueda_aleatoria(inversores, dinero, conflictos)

def ejemplo_3():
        inversores = ["A", "B", "C", "D", "E", "F", "G"]
        dinero = [1000000.0, 300000.0, 5.0, 5.0, 5.0, 5.0, 5.0]
        conflictos = {"A": {"B":{}, "C":{}, "D":{}, "E":{}, "F":{}, "G":{}}}
        return generar_busqueda_aleatoria(inversores, dinero, conflictos)


if __name__ == "__main__":
    main()