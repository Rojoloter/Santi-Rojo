import time
from sys import argv
from heap import Heap

from lectura import leer_ofertas, leer_restricciones

# solo para análisis
visitados = 0
poda_bt = 0
poda_bb = 0


def supera_restricciones(seleccionados, i, m, restricciones):
    if len(seleccionados) == 0:
        return True

    # i siempre es != a -1

    anterior = seleccionados[-1]

    if anterior != -1 and (i in restricciones[anterior] or anterior in restricciones[i]):
        return False

    if len(seleccionados) == m - 1:
        primero = seleccionados[0]

        if primero != -1 and (i in restricciones[primero] or primero in restricciones[i]):
            return False

    return True


def costo_1(v_r_anterior, persona, silla, ofertas):
    return v_r_anterior + ofertas[persona][silla]


def limite_1(v_e_anterior, persona, silla, ofertas, mejores):
    if persona == -1:
        return v_e_anterior - mejores[silla]
    return v_e_anterior - mejores[silla] + ofertas[persona][silla]


def limite_nm(v_r_anterior, persona, silla, ofertas, sel, m, n):
    s_sel = set(sel)
    v_e = v_r_anterior
    maximos = [-1] * (m - silla)
    for i in range(n):
        if i in s_sel:
            continue
        for s in range(silla+1, m):
            k = s - (silla+1)
            if maximos[k] < ofertas[i][s]:
                maximos[k] = ofertas[i][s]

    v_e += sum(maximos)

    if persona == -1:
        return v_e
    return v_e + ofertas[persona][silla]


def bb(m, n, restricciones, v_e_inicial, costo, limite):
    global visitados, poda_bt, poda_bb
    visitados += 1

    # (v_e, v_r, [persona en silla 1, ..., persona en silla m])
    heap = Heap[tuple[int, int, list[int]]](ascendant=False)
    v_max = 0
    sel_max = []

    heap.insert((v_e_inicial, 0, []))

    while (heap.not_empty()):
        visitados += 1

        v_e_sel, v_r_sel, sel = heap.extract()

        silla = len(sel)

        if silla == m:
            continue
        if v_e_sel < v_max:
            poda_bb += 1
            continue

        v_e_none = limite(v_e_sel, v_r_sel, -1, silla, sel)

        heap.insert((v_e_none, v_r_sel, sel + [-1]))

        s_sel = set(sel)

        for i in range(0, n):
            if i in s_sel:
                continue
            if not supera_restricciones(sel, i, m, restricciones):
                poda_bt += 1
                continue

            v_e_i = limite(v_e_sel, v_r_sel, i, silla, sel)
            if v_e_i < v_max:
                poda_bb += 1
                continue
            v_r_i = costo(v_e_sel, v_r_sel, i, silla, sel)
            sel_i = sel + [i]
            if v_r_i > v_max:
                v_max = v_r_i
                sel_max = sel_i
            heap.insert((v_e_i, v_r_i, sel_i))

    return v_max, sel_max


def main(argv, t):
    # if len(argv) != 3:
    #     print("Uso: python3 subasta_bb.py archivoOfertas.txt archivoRestricciones.txt")
    #     return 1
    # argv = ["", "ofertas.txt", "restricciones.txt"]  # TODO Borrar!!!
    i = 10
    # TODO Borrar!!!
    argv = ["", "tests/ofertas" +
            str(i)+".txt", "tests/restricciones"+str(i)+".txt"]

    m, nombres, ofertas = leer_ofertas(argv[1])
    restricciones = leer_restricciones(argv[2], nombres)

    # Preprocesamiento. TODO ver si se usa
    mejores_por_porcion = [-1] * m
    for j in range(m):
        mejores_por_porcion[j] = max(ofertas[i][j]
                                     for i in range(len(ofertas)))

    n = len(nombres)

    if t == 0:
        print("limite O(1)")
        maximo, seleccionados = bb(
            m, n,
            restricciones,
            sum(mejores_por_porcion),
            lambda v_e, v_r, persona, silla, sel: costo_1(
                v_r, persona, silla, ofertas),
            lambda v_e, v_r, persona, silla, sel: limite_1(v_e, persona, silla, ofertas, mejores_por_porcion) \
            # lambda v_e, v_r, persona, silla, sel: limite_nm(v_r, persona, silla, ofertas, sel, m, n)
        )
    else:
        print("limite O(nm)")
        maximo, seleccionados = bb(
            m, n,
            restricciones,
            sum(mejores_por_porcion),
            lambda v_e, v_r, persona, silla, sel: costo_1(v_r, persona, silla, ofertas), \
            # lambda v_e, v_r, persona, silla, sel: limite_1(v_e, persona, silla, ofertas, mejores_por_porcion)
            lambda v_e, v_r, persona, silla, sel: limite_nm(
                v_r, persona, silla, ofertas, sel, m, n)
        )

    print(f"La ganancia máxima a obtener es: {maximo}")

    seleccionados = seleccionados + \
        [-1] * (m - len(seleccionados))  # rellenar con -1 si faltan

    nombres_seleccionados = [nombres[i] if i != -
                             1 else "Vacío" for i in seleccionados]

    print("Los invitados ganadores son: " + ", ".join(nombres_seleccionados))


if __name__ == "__main__":
    start = time.time()
    main(argv, 0)
    print(f"\nNodos visitados: {visitados}")
    print(f"Podas por restricciones (BT): {poda_bt}")
    print(f"Podas por cota (BB): {poda_bb}")
    end = time.time()
    print(f"Tiempo de subasta_bb_new: {(end - start)*1000:.2f} ms")

    visitados = poda_bb = poda_bt = 0
    print()
    print()
    print()

    start = time.time()
    main(argv, 1)
    print(f"\nNodos visitados: {visitados}")
    print(f"Podas por restricciones (BT): {poda_bt}")
    print(f"Podas por cota (BB): {poda_bb}")
    end = time.time()
    print(f"Tiempo de subasta_bb_new: {(end - start)*1000:.2f} ms")
