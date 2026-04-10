import heapq
import grafo
import random
from collections import deque


def bfs(grafo,origen):
    visitados= set()
    padres={}
    orden={}
    padres[origen]= None
    orden[origen]=0
    visitados.add(origen)
    cola = deque()
    cola.append(origen)
    while len(cola) != 0:
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padres[w]=v
                orden[w]=orden[v]+1
                visitados.add(w)
                cola.append(w)
    return padres, orden

def camino_minimo_bf(grafo,origen):
    distancia={}
    padre={}
    for v in grafo.obtener_vertices():
        distancia[v]= float("inf")
    distancia[origen]= 0
    padre[origen]=None
    aristas=obtener_aristas(grafo)
    for i in range(len(grafo)):
        cambio= False
        for origen,destino,peso in aristas:
            if distancia[origen] + peso < distancia[destino]:
                cambio= True
                padre[destino]=origen
                distancia[destino]= distancia[origen]+peso
        if not cambio:
            return padre,distancia
        
    for v,w, peso in aristas:
        if distancia[v] + peso < distancia[w]:
            return None
    return padre,distancia

def camino_minimo_dijkstra(grafo,origen,destino):
    dist={}
    padre={}
    for v in grafo.obtener_vertices():
        dist[v]= float("inf")
    dist[origen]=0
    padre[origen]=None
    heap=[]
    heapq.heappush(heap,(0, origen))
    while len(heap) !=0:
        _,v= heapq.heappop(heap)
        if v == destino:
            return padre,dist
        for w in grafo.adyacentes(v):
            distancia= dist[v] + grafo.peso(v,w)
            if distancia < dist[w]:
                dist[w]= distancia
                padre[w]= v
                heapq.heappush(heap,(distancia[w], w))
    return padre,dist

def reconstruir_camino(padres, destino):
    recorrido = []
    while destino is not None:
        recorrido.append(destino)
        destino = padres[destino]
    return recorrido[::-1]

def cfc_grafo(grafo):
    resultados=[]
    visitados= set()
    for v in grafo.obtener_vertices():
        if v not in visitados:
            pila= deque()
            dfs_cfc(grafo,v,visitados,{},{},pila,set(),resultados,[0])
    return resultados

def dfs_cfc(grafo,v,visitados,orden,mas_bajo,pila,apilados,cfcs,contador_global):
    orden[v]= mas_bajo[v]=contador_global[0]
    contador_global[0]+=1
    visitados.add(v)
    pila.append(v)
    apilados.add(v)

    for w in grafo.adyacentes(v):
        if w not in visitados:
            dfs_cfc(grafo,w,visitados,orden,mas_bajo,pila,apilados,cfcs,contador_global)
        if w in apilados:
            mas_bajo[w]= min(mas_bajo[v],mas_bajo[w])
    if orden[v]== mas_bajo[v]:
        nueva_cfc= []
        while True:
            w=pila.pop()
            apilados.remove(w)
            nueva_cfc.append(w)
            if w == v:
                break
    cfcs.append(nueva_cfc)

def topologico_grados(grafo):
    g_ent= grados_entrada(grafo)
    cola = deque()
    for v in grafo.obtener_vertices():
        if g_ent[v]== 0:
            cola.append(v)
    resultado=[]

    while len(cola) != 0:
        v = cola.popleft()
        resultado.append(v)
        for w in grafo.adyacentes(v):
            g_ent[w]-=1
            if g_ent[w]== 0:
                cola.append(w)
    if len(resultado) != len(grafo.obtener_vertices()):
        raise ValueError(f"Hay un ciclo")
    return resultado

def contar_aristas(grafo):
    contador= 0
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            contador+=1
    return contador

def contar_componentes_conexas(grafo):
    visitados= set()
    comps= 0
    for v in grafo.obtener_vertices():
        if v not in visitados:
            comps+=1
            dfs_comps(grafo,v,visitados)

def dfs_comps(grafo,v,visitados,componente):
    visitados.add(v)
    componente.append(v)
    for w in grafo.adyacentes(v):
        if w not in visitados:
            dfs_comps(grafo,w,visitados,componente)

def recorrido_dfs(grafo):
    visitados= set()
    padres={}
    orden={}
    for v in grafo.obtener_vertices():
        if v not in visitados:
            visitados.add(v)
            padres[v]=None
            orden[v]= 0
            _dfs(grafo,v,visitados,padres,orden)
    return padres,orden

def _dfs(grafo,v,visitados,padres,orden):
    for w in grafo.adyacentes(v):
        if w not in visitados:
            visitados.add(w)
            padres[w]= v
            orden[w]=orden[v]+1
            _dfs(grafo,w,visitados,padres,orden)

def es_conexo(grafo):
    visitados= set()
    cola = deque()
    origen=random.choice(grafo.keys())
    visitados.add(origen)
    cola.append(origen)
    while len(cola) != 0:
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                cola.append(w)
                visitados.add(w)
    return len(visitados)== len(grafo)

def es_arbol(grafo):
    return es_conexo(grafo) and contar_aristas(grafo) == len(grafo) - 1


def grados_salida(grafo):
    gr={}
    for v in grafo.obtener_vertices():
        gr[v]= len(grafo.adyacentes(v))
    return gr

def grados_entrada(grafo):
    gr_entrada={}
    for v in grafo.obtener_vertices():
        gr_entrada[v]= 0
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            gr_entrada[w]+=1
    return gr_entrada

def obtener_aristas(grafo):
    resultado=[]
    visitados= set()
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            if w not in visitados:
                resultado.append((v,w))
        visitados.add(v)
    return resultado

PESO= 2
def find(self,v):
    if self.groups[v]== v:
        return v
    real_group= self.find(self.groups[v])
    self.groups[v]= real_group
    return real_group

def union(self,u,v):
    new_group= self.find(u)
    other=self.find(v)
    self.groups[other]= new_group



#vertices por comp conexas

def vertices(grafo):
    visitados= set()
    comps=0
    resultado=[]
    for v in grafo.obtener_vertices():
        if v not in visitados:
            nueva_componente=[]
            resultado.append(nueva_componente)
            comps+=1
            dfs_comps(grafo,v,visitados,nueva_componente)
    return resultado

def mst_prim(g):
    v=random.choice(grafo.keys())
    visitados=set()
    visitados.add(v)
    q= []
    for w in grafo.adyacentes(v):
        heapq.heappush(q, (g.peso_arista(v,w),v,w))
    arbol= grafo.Grafo(es_dirigido=False,lista_vertices=grafo.obtener_vertices())
    while len(q) != 0:
        peso,v,w = heapq.heappop(q)
        if w in visitados:
            continue
        arbol.agregar_arista(v,w,peso)
        visitados.add(w)
        for x in grafo.adyacentes(w):
            if x not in visitados:
                heapq.heappush(q,(g.peso_arista(w,x),w,x))
    return arbol


def ordenar_vertices(distancia):
    vertices_ordenados = sorted(distancia.keys(), key=lambda v:distancia[v], reverse=True)
    for indice, vertice in enumerate(vertices_ordenados):
        if distancia[vertice] == float("inf"):
            vertices_ordenados.pop(indice)
    return vertices_ordenados 