from grafo import Grafo

"""Se espera recibir:
Inversores = Lista de inversores
Dinero = Lista de floats, cada elemento de la lista corresponde al dinero invertido por el inversor del mismo índice
Conflictos: Diccionario de conflictos. Por cada item del diccionario, la clave tiene conflicto con los elementos del valor.
Se asume que los conflictos pueden ser unilaterales. EJ: {A: [B, C], B: [C]}. B no puede invertir junto a A a pesar de que no se considere en conflicto con A
"""
def ratio_inversores(inversores, dinero, conflictos):
    ratios = []
    g = Grafo()
    for k, v in conflictos.items():
        armar_grafo(k, v, g)

    i = 0
    for inversor in inversores:
        cant_conflictos = len(g.obtener_vecinos(inversor))
        r = dinero[i]/(cant_conflictos + 1)
        ratios.append((inversor, r))
        i += 1

    ratios = sorted(ratios, key=lambda x: x[1], reverse=True)
    seleccionados = []
    ganancia = 0
    for inversor, r in ratios:
        if not tiene_conflictos_con_seleccionados(inversor, seleccionados, g):
            seleccionados.append(inversor)
            ganancia += dinero[inversores.index(inversor)]
    return seleccionados, ganancia

def armar_grafo(k, v, g):
    if k not in g.obtener_vertices():
        g.agregar_vertice(k)
    for enemigo in v:
        if enemigo not in g.obtener_vertices():
            g.agregar_vertice(enemigo)
        g.agregar_arista(k, enemigo, 1)

def tiene_conflictos_con_seleccionados(inversor, seleccionados, g):
    vecinos = g.obtener_vecinos(inversor)
    for vecino in vecinos:
        if vecino in seleccionados:
            return True
    return False

#Óptimo = [B, C], 2100. Aproximado = [A], 2000. Grafo de incompatibilidades: B---A---C
def ejemplo_1():
    inversores = ["A", "B", "C"]
    dinero = [2000.0, 1100.0, 1000.0]
    conflictos = {"A": ["B", "C"]}
    return ratio_inversores(inversores, dinero, conflictos)

#Óptimo = Aproximado = [A, C, E], 275. Grafo de incompatibilidades: A---B---C---D---E
def ejemplo_2():
    inversores = ["A", "B", "C", "D", "E"]
    dinero = [100.0, 90.0, 95.0, 85.0, 80.0]
    conflictos = {"A": "B", "B": "C", "C": "D", "D": "E"}
    return ratio_inversores(inversores, dinero, conflictos)

#Óptimo = [A], 1000000. Aproximado = 300025. Grafo de incompatibilidades: grafo estrella con centro A
def ejemplo_3():
    inversores = ["A", "B", "C", "D", "E", "F", "G"]
    dinero = [1000000.0, 300000.0, 5.0, 5.0, 5.0, 5.0, 5.0]
    conflictos = {"A": ["B", "C", "D", "E", "F", "G"]}
    return ratio_inversores(inversores, dinero, conflictos)

def main():
    print(f"Ejemplo 1: {ejemplo_1()}. Óptimo: (['B', 'C'], 2100.0)")
    print(f"Ejemplo 2: {ejemplo_2()}. Óptimo: (['A', 'C', 'E'], 275.0)")
    print(f"Ejemplo 3: {ejemplo_3()}. Óptimo: (['A'], 1000000.0)")

if __name__ == "__main__":
    main()
