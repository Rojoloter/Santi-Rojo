import sys
from heap import Heap

from lectura import leer_ofertas, leer_restricciones


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

# obtiene la ganancia en O(1)


def valor_real_1(v_r_anterior, persona, silla, ofertas):
    return v_r_anterior + ofertas[persona][silla]


""" 
Testeado que es peor que la otra poda
# Obtiene la ganancia estimada en O(1)
def estimado_1(v_e_anterior, persona, silla, ofertas, mejores): # O(1)
    if persona == -1:
        return v_e_anterior - mejores[silla]
    return v_e_anterior - mejores[silla] + ofertas[persona][silla] 
 """

# Obtiene el valor estimado en O(n*m)
# El valor estimado es bastante bueno


def estimado_nm(v_r_anterior, persona, silla, ofertas, sel, m, n):  # O(n * m)
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


def branch_and_bound(m, n, restricciones, v_e_inicial, obtener_v_r, obtener_v_e):
    # (v_e, v_r, [persona en silla 1, ..., persona en silla m])
    heap = Heap[tuple[int, int, list[int]]](ascendant=False)
    v_max = 0
    sel_max = []

    heap.insert((v_e_inicial, 0, []))

    while (heap.not_empty()):
        v_e_sel, v_r_sel, sel = heap.extract()

        silla = len(sel)

        if silla == m:
            continue
        if v_e_sel < v_max:
            print("Poda 1", sel)
            continue

        v_e_none = obtener_v_e(v_e_sel, v_r_sel, -1, silla, sel)

        heap.insert((v_e_none, v_r_sel, sel + [-1]))

        s_sel = set(sel)

        for i in range(0, n):
            if i in s_sel:
                continue
            if not supera_restricciones(sel, i, m, restricciones):
                print("Poda BT", sel, i)
                continue

            v_e_i = obtener_v_e(v_e_sel, v_r_sel, i, silla, sel)  # nm
            if v_e_i < v_max:
                print("Poda x Estimado")
                continue
            v_r_i = obtener_v_r(v_e_sel, v_r_sel, i, silla, sel)
            sel_i = sel + [i]
            if v_r_i > v_max:
                v_max = v_r_i
                sel_max = sel_i
            heap.insert((v_e_i, v_r_i, sel_i))  # log(n!n) = nlog(n)

    return v_max, sel_max


def main(argv):
    argv = ["", "o.txt", "r.txt"]
    m, nombres, ofertas = leer_ofertas(argv[1])
    restricciones = leer_restricciones(argv[2], nombres)

    mejores_por_porcion = [-1] * m
    for j in range(m):
        mejores_por_porcion[j] = max(ofertas[i][j]
                                     for i in range(len(ofertas)))

    n = len(nombres)

    maximo, seleccionados = branch_and_bound(
        m, n,
        restricciones,
        sum(mejores_por_porcion),
        lambda v_e, v_r, persona, silla, sel: valor_real_1(v_r, persona, silla, ofertas), \
        # lambda v_e, v_r, persona, silla, sel: estimado_1(v_e, persona, silla, ofertas, mejores_por_porcion)
        lambda v_e, v_r, persona, silla, sel: estimado_nm(
            v_r, persona, silla, ofertas, sel, m, n)
    )

    print(f"La ganancia máxima a obtener es: {maximo}")

    # rellenar con -1 si faltan
    seleccionados = seleccionados + [-1] * (m - len(seleccionados))

    nombres_seleccionados = [nombres[i] if i != -
                             1 else "Vacío" for i in seleccionados]

    print("Los invitados ganadores son: " + ", ".join(nombres_seleccionados))


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Uso: python3 subasta_bb.py archivoOfertas.txt archivoRestricciones.txt")
    #     sys.exit(1)
    main(sys.argv)
