class Grafo:
    def __init__(self):
        # Diccionario de adyacencia: {origen: {destino: capacidad, ...}, ...}
        self.adyacencia = {}

    def agregar_vertice(self, nombre):
        if nombre not in self.adyacencia:
            self.adyacencia[nombre] = {}

    def agregar_arista(self, origen, destino, capacidad):
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self.adyacencia[origen][destino] = capacidad
        self.adyacencia[destino][origen] = capacidad

    def eliminar_arista(self, origen, destino):
        if origen in self.adyacencia and destino in self.adyacencia[origen]:
            del self.adyacencia[origen][destino]
            del self.adyacencia[destino][origen]

    def obtener_vecinos(self, origen):
        return self.adyacencia.get(origen, {})

    def obtener_vertices(self):
        return list(self.adyacencia.keys())

    def existe_arista(self, origen, destino):
        return destino in self.adyacencia.get(origen, {})

    def capacidad(self, origen, destino):
        return self.adyacencia[origen].get(destino, 0)

    def set_capacidad(self, origen, destino, capacidad):
        self.adyacencia[origen][destino] = capacidad

    def copy(self):
        nuevo = Grafo()
        for origen in self.adyacencia:
            nuevo.adyacencia[origen] = self.adyacencia[origen].copy()
        return nuevo
