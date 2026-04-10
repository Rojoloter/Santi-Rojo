import random

def monte_carlo_inversores(inversores, dinero, conflictos, iteraciones=30):

    mejor_seleccion = []
    mejor_valor = 0

    # Crear mapeo inversor -> índice para fácil acceso
    indice_inversor = {inv: i for i, inv in enumerate(inversores)} #n

    for _ in range(iteraciones):
        seleccion_actual = []
        valor_actual = 0
        inversores_disponibles = inversores.copy()

        while inversores_disponibles: #O(n)

            inversor_elegido = random.choice(inversores_disponibles) #O(log n)

            # Agregar inversor a la selección
            seleccion_actual.append(inversor_elegido)
            valor_actual += dinero[indice_inversor[inversor_elegido]]

            # Eliminar inversor elegido y todos sus conflictos
            inversores_a_eliminar = obtener_todos_los_conflictos(inversor_elegido, conflictos, inversores_disponibles)

            for inv in inversores_a_eliminar: #O(n)
                if inv in inversores_disponibles:
                    inversores_disponibles.remove(inv)

        if valor_actual > mejor_valor:
            mejor_valor = valor_actual
            mejor_seleccion = seleccion_actual.copy()

    return mejor_seleccion, mejor_valor


def obtener_todos_los_conflictos(inversor_elegido, conflictos, inversores_disponibles):

    inversores_a_eliminar = [inversor_elegido]

    # Agregar conflictos directos (inversor_elegido -> otros)
    if inversor_elegido in conflictos:
        for conflicto in conflictos[inversor_elegido]:
            inversores_a_eliminar.append(conflicto)

    # Agregar conflictos inversos (otros -> inversor_elegido)
    for inv in inversores_disponibles:
        if inv in conflictos and inversor_elegido in conflictos[inv]:
            inversores_a_eliminar.append(inv)

    return inversores_a_eliminar

# Función de ejemplo para probar
def main():

    print(f"Ejemplo 1: {ejemplo_1()}. Óptimo: (['B', 'C'], 2100.0)")
    print(f"Ejemplo 2: {ejemplo_2()}. Óptimo: (['A', 'C', 'E'], 275.0)")
    print(f"Ejemplo 3: {ejemplo_3()}. Óptimo: (['A'], 1000000.0)")

#Óptimo = [B, C], 2100. Aproximado = [A], 2000. Grafo de incompatibilidades: B---A---C
def ejemplo_1():
    inversores = ["A", "B", "C"]
    dinero = [2000.0, 1100.0, 1000.0]
    conflictos = {"A": ["B", "C"]}
    return monte_carlo_inversores(inversores, dinero, conflictos)

#Óptimo = Aproximado = [A, C, E], 275. Grafo de incompatibilidades: A---B---C---D---E
def ejemplo_2():
    inversores = ["A", "B", "C", "D", "E"]
    dinero = [100.0, 90.0, 95.0, 85.0, 80.0]
    conflictos = {"A": "B", "B": "C", "C": "D", "D": "E"}
    return monte_carlo_inversores(inversores, dinero, conflictos)

#Óptimo = [A], 1000000. Aproximado = 300025. Grafo de incompatibilidades: grafo estrella con centro A
def ejemplo_3():
    inversores = ["A", "B", "C", "D", "E", "F", "G"]
    dinero = [1000000.0, 300000.0, 5.0, 5.0, 5.0, 5.0, 5.0]
    conflictos = {"A": ["B", "C", "D", "E", "F", "G"]}
    return monte_carlo_inversores(inversores, dinero, conflictos)


if __name__ == "__main__":
    main()