from sys import argv


def mezclar_y_contar_inversiones(lista, izq, der):
    i = j = inversiones = 0
    while i < len(izq) and j < len(der):
        if izq[i] < der[j]:
            lista[i + j] = izq[i]
            i += 1
        else:
            lista[i + j] = der[j]
            j += 1
            inversiones += len(izq) - i
    lista[i + j:] = (  # copia el resto
        izq[i:] if i < len(izq) else der[j:]
    )
    return inversiones


def ordenar_y_contar_inversiones(lista):
    inversiones = 0
    if len(lista) > 1:
        medio = len(lista) // 2
        izq = lista[:medio]
        der = lista[medio:]
        inversiones += ordenar_y_contar_inversiones(izq)
        inversiones += ordenar_y_contar_inversiones(der)
        inversiones += mezclar_y_contar_inversiones(lista, izq, der)
    return inversiones


def leer_barrios(nombre_archivo):
    norte = {}
    sur = {}
    with open(nombre_archivo) as f:
        for i, barrio in enumerate(f):
            if barrio.strip() == "":
                break
            norte[barrio.strip()] = i
        for i, barrio in enumerate(f):
            sur[barrio.strip()] = i
    return norte, sur


def leer_propuesta(nombre_archivo, norte, sur):
    propuesta = [0] * len(norte)
    with open(nombre_archivo) as f:
        for linea in f:
            puente = linea.strip().split(",")
            ind_norte = norte[puente[0].strip()]
            ind_sur = sur[puente[1].strip()]
            propuesta[ind_norte] = ind_sur
    return propuesta


def main(argv):

    if len(argv) != 3:
        print("Uso: python puentes_dq.py archivoBarrios.txt archivoPropuesta.txt")
        return 1

    norte, sur = leer_barrios(argv[1])

    propuesta = leer_propuesta(argv[2], norte, sur)

    inversiones = ordenar_y_contar_inversiones(propuesta)
    print(inversiones)


if __name__ == "__main__":
    main(argv)
