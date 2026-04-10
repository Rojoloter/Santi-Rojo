# solo para debug/seguimiento
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp


def imprimir_grafo(grafo, titulo="Grafo"):
    print(f"--- {titulo} ---")
    for origen in grafo.obtener_vertices():
        for destino, capacidad in grafo.obtener_vecinos(origen).items():
            print(f"{origen} --({capacidad})--> {destino}")
    print()


def imprimir_flujo_final(grafo_original, grafo_residual):
    for origen in grafo_original.obtener_vertices():
        for destino, capacidad in grafo_original.obtener_vecinos(origen).items():
            capacidad_residual = grafo_residual.capacidad(origen, destino)
            flujo_usado = capacidad - capacidad_residual
            print(f"{origen} --({flujo_usado}/{capacidad})--> {destino}")


def visualizar_flujo(grafo_original, grafo_residual, titulo="Flujo utilizado"):
    G = nx.DiGraph()

    for origen in grafo_original.adyacencia:
        for destino, capacidad in grafo_original.adyacencia[origen].items():
            capacidad_residual = grafo_residual.capacidad(origen, destino)
            flujo_utilizado = capacidad - capacidad_residual
            etiqueta = f"{flujo_utilizado}/{capacidad}"
            G.add_edge(origen, destino, label=etiqueta)

    # pos = nx.spring_layout(G, seed=42)
    # pos = nx.shell_layout(G)
    pos = nx.kamada_kawai_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=1000, font_size=10, arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(titulo)
    plt.show()


# solo para debug/seguimiento
def visualizar_grafo(grafo, titulo="Grafo con Capacidades"):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()

    for origen, vecinos in grafo.adyacencia.items():
        for destino, capacidad in vecinos.items():
            G.add_edge(origen, destino, capacity=capacidad)

    pos = nx.kamada_kawai_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'capacity')

    plt.figure(figsize=(8, 6))

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800)
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Dibujar aristas con curvatura
    nx.draw_networkx_edges(
        G, pos,
        connectionstyle='arc3,rad=0.2',
        arrows=True,
        arrowstyle='-|>',
        arrowsize=20,
        edge_color='black',
        width=1.5
    )

    # Dibujar etiquetas de aristas evitando superposición
    for (origen, destino), capacidad in edge_labels.items():
        x1, y1 = pos[origen]
        x2, y2 = pos[destino]
        dx, dy = x2 - x1, y2 - y1
        xm, ym = x1 + dx * 0.5, y1 + dy * 0.5

        # Desplazamiento ortogonal
        offset = 0.05
        normal = (-dy, dx)
        length = (normal[0]**2 + normal[1]**2)**0.5
        normal = (normal[0]/length, normal[1]/length)

        # Etiqueta desplazada si hay arista opuesta
        if G.has_edge(destino, origen):
            xm += offset * normal[0]
            ym += offset * normal[1]

        plt.text(xm, ym, str(capacidad), fontsize=9, bbox=dict(
            facecolor='white', edgecolor='none', pad=1))

    plt.title(titulo)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
