import sys
from grafo import Grafo
from edmons_karp import edmons_karp


def leer_ciudades(nombre_archivo, grafo, s):
    with open(nombre_archivo) as f:
        for vuelo in f:
            ciudades = vuelo.strip().split(",")
            grafo.agregar_arista(ciudades[0]+'i', ciudades[0]+'o', s)
            grafo.agregar_arista(ciudades[1]+'i', ciudades[1]+'o', s)
            grafo.agregar_arista(ciudades[0]+'o', ciudades[1]+'i', s)
            grafo.agregar_arista(ciudades[1]+'o', ciudades[0]+'i', s)


def leer_espias(nombre_archivo, grafo, n):
    with open(nombre_archivo) as f:
        espias = []
        for i in range(n):
            espia = f.readline().strip().split(",")
            espias.append(espia)
            if grafo.existe_arista('Fuente', espia[1]+'i'):
                grafo.set_capacidad(
                    'Fuente', espia[1]+'i', grafo.capacidad('Fuente', espia[1]+'i')+1)
            else:
                grafo.agregar_arista('Fuente', espia[1]+'i', 1)
        centros = []
        for i in range(n):
            centro = f.readline().strip().split(",")
            centros.append(centro)
            grafo.agregar_arista(centro[1]+'o', 'Sumidero', 1)
    return espias, centros


def obtener_rutas(grafo_original, grafo_residual, espias, centros):
    lista_flujo: list[tuple[str, str, int]] = []
    # Construye la tabla de flujo a partir del grafo original y del residual
    # Sin la Fuente y sin los nodos duplicados
    # Para armar las rutas va a partir de los espías y no de la Fuente.
    for origen in grafo_original.obtener_vertices():
        for destino, capacidad in grafo_original.obtener_vecinos(origen).items():
            capacidad_residual = grafo_residual.capacidad(origen, destino)
            flujo = capacidad - capacidad_residual
            if origen[:-1] != destino[:-1]:
                if destino == 'Sumidero':
                    lista_flujo.append((origen[:-1], 'Sumidero', flujo))
                elif origen != 'Fuente':
                    lista_flujo.append((origen[:-1], destino[:-1], flujo))

    # Arma las rutas de cada espía
    rutas = []
    for espia in espias:
        ruta = [espia[0]]
        destino = espia[1]

        while (destino != 'Sumidero'):
            origen = destino

            for i, (origen_f, destino_f, flujo) in enumerate(lista_flujo):
                if origen_f == origen and flujo > 0:
                    break

            ruta.append(origen)

            lista_flujo[i] = (origen_f, destino_f, flujo-1)

            destino = destino_f

        for centro in centros:
            if centro[1] == origen:
                ruta.append(centro[0])

        rutas.append(ruta)

    return (rutas)


def main(argv):

    n = int(argv[1])
    s = int(argv[2])

    grafo = Grafo()

    leer_ciudades(argv[3], grafo, s)
    espias, centros = leer_espias(argv[4], grafo, n)

    flujo, grafo_residual = edmons_karp(grafo, "Fuente", "Sumidero")

    if flujo < n:
        print("“Es imposible lograr el objetivo”")
    else:
        rutas = obtener_rutas(grafo, grafo_residual, espias, centros)
        for ruta in rutas:
            print(", ".join(ruta))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python3 traslado.py n s archivoCiudades.txt archivoEspias.txt")
        sys.exit(1)
    main(sys.argv)
