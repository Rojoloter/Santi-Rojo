from collections import deque
from grafo import Grafo


def bfs(grafo, fuente, sumidero):
    padres = {fuente: None}
    cola = deque([fuente])
    while cola:
        origen = cola.popleft()
        for destino in grafo.obtener_vecinos(origen):
            if destino not in padres:
                padres[destino] = origen
                if destino == sumidero:
                    return padres
                cola.append(destino)
    return None


def flujo_minimo(grafo, camino, inicio, fin):
    # Encontrar cuello de botella en el camino
    minimo = float('inf')
    destino = fin
    while destino != inicio:
        origen = camino[destino]
        minimo = min(minimo, grafo.capacidad(origen, destino))
        destino = origen
    return minimo


def edmons_karp(grafo_original, fuente, sumidero):
    grafo_residual = grafo_original.copy()

    flujo_maximo = 0

    while True:
        camino = bfs(grafo_residual, fuente, sumidero)
        if camino is None:
            break

        flujo_min = flujo_minimo(grafo_residual, camino, fuente, sumidero)

        # actualizar grafo residual
        destino = sumidero
        while destino != fuente:
            origen = camino[destino]
            grafo_residual.set_capacidad(
                origen, destino, grafo_residual.capacidad(origen, destino) - flujo_min)
            grafo_residual.set_capacidad(
                destino, origen, grafo_residual.capacidad(destino, origen) + flujo_min)
            if grafo_residual.capacidad(origen, destino) == 0:
                grafo_residual.eliminar_arista(origen, destino)
            destino = origen

        flujo_maximo += flujo_min

    return flujo_maximo, grafo_residual
