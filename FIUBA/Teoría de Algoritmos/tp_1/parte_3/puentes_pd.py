from sys import argv


def buscar_posicion(sub, num):
    izq = 0
    der = len(sub)
    while izq < der:
        medio = (izq + der) // 2
        if sub[medio] < num:
            izq = medio + 1
        else:
            der = medio
    return izq


def secuencia_creciente_mas_larga(secuencia):
    finales_minimos = []
    prev = [-1] * len(secuencia)
    indices = [-1] * len(secuencia)

    for i, num in enumerate(secuencia):
        pos = buscar_posicion(finales_minimos, num)

        if pos == len(finales_minimos):
            finales_minimos.append(num)
        else:
            finales_minimos[pos] = num

        if pos > 0:
            prev[i] = indices[pos - 1]

        indices[pos] = i

    # Reconstrucción de la subsecuencia más larga
    max_sub_sequencia = []
    index = indices[len(finales_minimos) - 1]
    while index != -1:
        max_sub_sequencia.append(secuencia[index])
        index = prev[index]

    max_sub_sequencia.reverse()

    return max_sub_sequencia


def leer_barrios(nombre_archivo):
    dic_norte = {}
    dic_sur = {}
    lista_norte = []
    lista_sur = []
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        for i, barrio in enumerate(f):
            barrio = barrio.strip()
            if barrio == "":
                break
            dic_norte[barrio] = i
            lista_norte.append(barrio)
        for i, barrio in enumerate(f):
            barrio = barrio.strip()
            dic_sur[barrio] = i
            lista_sur.append(barrio)
    return dic_norte, dic_sur, lista_norte, lista_sur


def leer_propuesta(nombre_archivo, dic_norte, dic_sur):
    propuesta = [0] * len(dic_norte)
    ind_a_norte = [0] * len(dic_norte)
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            puente = linea.strip().split(",")
            ind_norte = dic_norte[puente[0].strip()]
            ind_sur = dic_sur[puente[1].strip()]
            propuesta[ind_norte] = ind_sur
            ind_a_norte[ind_sur] = ind_norte
    return propuesta, ind_a_norte


def main(argv):

    if len(argv) != 3:
        print("Uso: python puentes_pd.py archivoBarrios.txt archivoPropuesta.txt")
        return 1

    dic_norte, dic_sur, lista_norte, lista_sur = leer_barrios(argv[1])

    propuesta, ind_a_norte = leer_propuesta(argv[2], dic_norte, dic_sur)

    max_secuencia = secuencia_creciente_mas_larga(propuesta)

    print("Se pueden construir", len(max_secuencia), "puentes")

    for numero in max_secuencia:
        print(lista_norte[ind_a_norte[numero]], "=>", lista_sur[numero])


if __name__ == "__main__":
    main(argv)
