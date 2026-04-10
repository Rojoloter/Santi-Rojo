import sys

from lectura import leer_ofertas, leer_restricciones


def supera_restricciones(seleccionados, i, m, restricciones):

    if len(seleccionados) == 0:  # para que exista seleccionados[-1]
        return True

    anterior = seleccionados[-1]

    if i is not None and anterior in restricciones[i]:
        return False

    if anterior is not None and i in restricciones[anterior]:
        return False

    if len(seleccionados) == m - 1:
        primero = seleccionados[0]

        if i is not None and primero in restricciones[i]:
            return False

        if primero is not None and i in restricciones[primero]:
            return False

    return True


def bt_rec(seleccionados, m, n, restricciones, resultados: list[list]):
    global visitados, poda_bt
    if len(seleccionados) == m:
        return resultados.append(seleccionados)

    bt_rec(seleccionados + [None], m, n, restricciones, resultados)

    s_seleccionados = set(seleccionados)
    for i in range(seleccionados[0]+1, n):
        if i in s_seleccionados:
            continue
        if not supera_restricciones(seleccionados, i, m, restricciones):
            continue
        bt_rec(seleccionados + [i], m, n, restricciones, resultados)


def backtracking(m, n, restricciones):
    resultados = []
    for i in range(n):
        bt_rec([i], m, n, restricciones, resultados)
    return resultados


def buscar_max_en_rotaciones(factibles, ofertas):
    maximo = -1
    seleccionados = []
    for factible in factibles:
        for _ in range(len(factible)):
            ganancia = 0
            for porcion in range(len(factible)):
                invitado = factible[porcion]
                if invitado is not None:
                    ganancia += ofertas[invitado][porcion]
            if ganancia > maximo:
                maximo = ganancia
                seleccionados = factible[:]
            factible = factible[1:]+[factible[0]]
    return maximo, seleccionados


def main(argv):

    m, nombres, ofertas = leer_ofertas(argv[1])
    restricciones = leer_restricciones(argv[2], nombres)

    factibles = backtracking(m, len(nombres), restricciones)

    maximo, seleccionados = buscar_max_en_rotaciones(factibles, ofertas)

    print(f"La ganancia máxima a obtener es: {maximo}")
    nombres_seleccionados = [
        nombres[i] if i is not None else "Vacío" for i in seleccionados
    ]
    print("Los invitados ganadores son: " + ", ".join(nombres_seleccionados))


if len(sys.argv) != 3:
    print("Uso: python3 subasta_bt_bf.py archivoOfertas.txt archivoRestricciones.txt")
    sys.exit(1)
main(sys.argv)
