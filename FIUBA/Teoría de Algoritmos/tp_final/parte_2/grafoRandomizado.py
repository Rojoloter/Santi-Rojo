#NO SE UTILIZA
class Grafo:
    def __init__(self):
        # Diccionario de adyacencia: {origen: {destino: capacidad, ...}, ...}
        self.adyacencia = {}
        # Diccionario de valores: {vertice1: valor1, vertice2: valor2, ...   verticeN: valorN}
        self.valores = {}
        # Contador de aristas
        self.aristas = 0

    def agregar_vertice(self, nombre, valor):
        if nombre not in self.adyacencia:
            self.adyacencia[nombre] = {}
            self.valores[nombre] = valor
    
    def eliminar_vertice_sin_vecinos(self, nombre):
        self.valores.pop(nombre)
        self.adyacencia.pop(nombre)
        return 0
    
    def agregar_vecindades(self, vecinos:dict):
        if(not vecinos):
            return 0
        for vecino in vecinos.keys():
            for vecinoDelVecino in vecinos[vecino].keys():
                self.agregar_arista(vecino,vecinoDelVecino, 0)
        return 0


    def eliminar_vecindades(self, nombre):
        vecinosEliminados = {}
        vecinos = list(self.obtener_vecinos(nombre))
        for vecino in vecinos:
            vecinosVecino = list(self.obtener_vecinos(vecino))
            vecinosEliminados[vecino] = {}
            for vecinoDelVecino in vecinosVecino:
                self.eliminar_arista(vecino, vecinoDelVecino)
                vecinosEliminados[vecino][vecinoDelVecino] = {}
        return vecinosEliminados

    def cantidad_vertices(self):
        return len(self.valores.keys())
    
    def agregar_arista(self, origen, destino, capacidad):
        self.aristas += 1
        self.agregar_vertice(origen, self.obtener_valor(origen))
        self.agregar_vertice(destino, self.obtener_valor(destino))
        self.adyacencia[origen][destino] = capacidad
        self.adyacencia[destino][origen] = capacidad

    def obtener_valor(self, nombre):
        return self.valores[nombre]
    
    def eliminar_arista(self, origen, destino):
        self.aristas -= 1
        if origen in self.adyacencia and destino in self.adyacencia[origen]:
            del self.adyacencia[origen][destino]
            del self.adyacencia[destino][origen]
        return 0

    def obtener_vecinos(self, origen):
        return self.adyacencia.get(origen, {})
    
    def vertices_sin_vecinos(self):
        vertices = {}
        for i in self.adyacencia.keys():
            if(not self.adyacencia[i]):
                vertices[i] = self.valores[i]
        return vertices
    
    def vertices_con_vecinos(self):
        vertices = {}
        for i in self.adyacencia.keys():
            if(self.adyacencia[i]):
                vertices[i] = self.valores[i]
        return vertices

    def obtener_vertices(self):
        vertices = {}
        for i in self.adyacencia.keys():
                vertices[i] = self.valores[i]
        return vertices
    
    def valor_grafo(self):
        contador = 0
        for i in self.valores.keys():
            contador += self.valores[i]
        return contador

    
    def obtener_aristas(self):
        return int(self.aristas)

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