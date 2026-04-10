import pulp
from pulp import LpProblem, LpVariable, LpMaximize, value, LpStatus, PULP_CBC_CMD
import math
from typing import cast

def problema_inicial():
    problema = LpProblem("personal_para_proyectos", LpMaximize)
    x1 = LpVariable("A", lowBound=0)
    x2 = LpVariable("B", lowBound=0)
    x3 = LpVariable("C", lowBound=0)

    problema += x1 + x2 + 3 * x3 <= 17, "Restriccion_ingenieros"
    problema += 3 * x1 + 2 * x2 + 2 * x3 <= 11, "Restriccion_disenadores"

    problema += 200 * x1 + 100 * x2 + 300 * x3

    return problema

def obtener_solucion(problema: LpProblem):
    solucion = problema.variables()
    valores = [cast(float, value(x)) for x in solucion]
    return valores

def elegir_variable_fraccional(problema: LpProblem):
    sel = 0
    valores = obtener_solucion(problema)
    for i, x in enumerate(valores):
        minimo = abs(0.5 - (valores[sel] - math.floor(valores[sel])))
        actual = abs(0.5 - (x - math.floor(x)))
        if actual < minimo:
            sel = i
    return sel, valores[sel], problema.variables()[sel]

def main():
    mejor_valor: float=float('-inf')
    solucion: list[int] | None = None
    def branch_and_bound(problema: LpProblem) -> None:
        nonlocal mejor_valor, solucion

        problema.solve(PULP_CBC_CMD(msg=False))

        if LpStatus[problema.status] != "Optimal":
            return
        assert problema.objective is not None
        valor_objetivo = cast(float, value(problema.objective))
        if valor_objetivo <= mejor_valor:
            return

        i, numero, x = elegir_variable_fraccional(problema)

        #Si la variable es entera, todas las variables son enteras y se encontró una solución entera optima para las restricciones actuales. Seguir por esta rama no aumentará la ganancia.
        if numero.is_integer():
            if valor_objetivo > mejor_valor:
                solucion = [int(x) for x in obtener_solucion(problema)]
                mejor_valor = valor_objetivo
            return

        #Se puede calcular una cota inferior para podar en las siguientes ramificaciones
        coeficientes = [cast(float, coef) for coef in problema.objective.values()]
        x_enteros = [math.floor(x) for x in obtener_solucion(problema)]
        cota_inferior = sum(coef * x for coef, x in zip(coeficientes, x_enteros))
        if cota_inferior > mejor_valor:
            mejor_valor = cota_inferior
            solucion = x_enteros

        piso = math.floor(numero)
        techo = math.ceil(numero)

        problema_izq = problema.copy()
        problema_izq += x <= piso
        branch_and_bound(problema_izq)

        problema_der = problema.copy()
        problema_der += x >= techo
        branch_and_bound(problema_der)
    
    branch_and_bound(problema_inicial())


    if solucion:
        x1, x2, x3 = solucion
        ingenieros = 17 - x1 - x2 - 3 * x3
        disenadores = 11 - 3 * x1 - 2 * x2 - 2 * x3
        print("Solución entera óptima encontrada:")
        print("Ganancia:", mejor_valor)
        print("Proyectos tipo A:", x1)
        print("Proyectos tipo B:", x2)
        print("Proyectos tipo C:", x3)
        print(f"Recursos restantes: Ingenieros = {ingenieros}, Diseñadores = {disenadores}")
    else:
        print("No se encontró solución entera.")


if __name__ == "__main__":
    main()
