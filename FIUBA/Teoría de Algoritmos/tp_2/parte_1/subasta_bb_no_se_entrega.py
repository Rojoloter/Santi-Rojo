import time
from sys import argv

from lectura import leer_ofertas, leer_restricciones

# solo para análisis
visitados = 0
poda_bt = 0
poda_bb = 0


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


def cota_superior(ofertas, seleccionados, m, mejores_por_porcion):
    cota = 0
    # Esto es O(m)
    # Pero poda menos!!!
    for i in range(m):
        if i < len(seleccionados):
            invitado = seleccionados[i]
            if invitado is not None:
                cota += ofertas[invitado][i]
        else:
            cota += mejores_por_porcion[i]
    return cota


def bb(mejor_ganancia, seleccionados, m, ofertas, restricciones, mejores_por_porcion):
    global visitados, poda_bt, poda_bb
    visitados += 1

    if len(seleccionados) == m:
        ganancia = 0
        for i in range(m):
            invitado = seleccionados[i]
            if invitado is not None:
                ganancia += ofertas[invitado][i]
        return ganancia, seleccionados

    candidatos = []

    nueva_sel = seleccionados + [None]
    cota = cota_superior(ofertas, nueva_sel, m, mejores_por_porcion)
    if cota > mejor_ganancia:
        candidatos.append((cota, None))
    else:
        poda_bb += 1

    s_seleccionados = set(seleccionados)
    for i in range(len(ofertas)):
        if i in s_seleccionados:
            continue
        if not supera_restricciones(seleccionados, i, m, restricciones):
            poda_bt += 1
            continue
        nueva_sel = seleccionados + [i]
        cota = cota_superior(
            ofertas, nueva_sel, m, mejores_por_porcion)
        if cota <= mejor_ganancia:
            poda_bb += 1
            continue
        candidatos.append((cota, i))

    candidatos.sort(key=lambda x: x[0], reverse=True)

    mejor_seleccion = []

    for cota, i in candidatos:
        if cota > mejor_ganancia:
            nueva_sel = seleccionados + [i]
            ganancia_actual, seleccion_actual = bb(
                mejor_ganancia, nueva_sel, m, ofertas, restricciones, mejores_por_porcion)
            if ganancia_actual > mejor_ganancia:
                mejor_ganancia = ganancia_actual
                mejor_seleccion = seleccion_actual

    return mejor_ganancia, mejor_seleccion


def main(argv):
    # if len(argv) != 3:
    #     print("Uso: python3 subasta_bb.py archivoOfertas.txt archivoRestricciones.txt")
    #     return 1
    # argv = ["", "ofertas.txt", "restricciones.txt"]  # TODO Borrar!!!
    i = 2
    # TODO Borrar!!!
    argv = ["", "tests/ofertas" +
            str(i)+".txt", "tests/restricciones"+str(i)+".txt"]

    m, nombres, ofertas = leer_ofertas(argv[1])
    restricciones = leer_restricciones(argv[2], nombres)

    # Preprocesamiento. TODO ver si se usa
    mejores_por_porcion = [
        max(ofertas[i][j] for i in range(len(ofertas)))
        for j in range(m)
    ]

    maximo, seleccionados = bb(-1, [], m, ofertas,
                               restricciones, mejores_por_porcion)

    print(f"La ganancia máxima a obtener es: {maximo}")
    nombres_seleccionados = [
        nombres[i] if i is not None else "Vacío" for i in seleccionados
    ]
    print("Los invitados ganadores son: " + ", ".join(nombres_seleccionados))


if __name__ == "__main__":
    start = time.time()
    main(argv)
    print(f"\nNodos visitados: {visitados}")
    print(f"Podas por restricciones (BT): {poda_bt}")
    print(f"Podas por cota (BB): {poda_bb}")
    end = time.time()
    print(f"Tiempo de subasta_bb_new: {(end - start)*1000:.2f} ms")
