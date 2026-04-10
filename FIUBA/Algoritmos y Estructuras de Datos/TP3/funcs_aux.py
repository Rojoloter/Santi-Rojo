import biblioteca
import grafo
import csv

OR_INV = "Origen inválido"
SIN_REC = "No se encontro recorrido"
ART_INV = "Artículo inválido"
PAG_404 = "No se encuentra la pagina"
LIM_ARTICULOS = 21

def listar_operaciones():
    operaciones = ["camino", "rango", "diametro", "navegacion", "clustering", "lectura"]
    for op in operaciones:
        print (op)

def crear_grafo_art (ruta, g, articulos):
    with open(ruta) as f:
        tsv_f = csv.reader(f, delimiter="\t")
        for linea in tsv_f:
            origen = linea[0]
            visitados = {}
            if origen not in articulos:
                g.agregar_vertice(origen)
                articulos[origen] = []
            cont = 0
            for w in linea:
                if cont == 0:
                    cont = 1 #Así saltea el mismo origen, pero permite que un articulo se autoreferencie
                    continue
                if w not in articulos:
                    articulos[w] = []
                    g.agregar_vertice(w)
                if w not in visitados:
                    g.agregar_arista(origen, w)
                    visitados[w] = []


def camino(g, origen, destino, articulos):
    if origen not in articulos:
        print (OR_INV)
    else:
        padres, orden = biblioteca.bfs(g, origen)
        if destino not in padres:
            print (SIN_REC)
        else:
            recorrido = biblioteca.reconstruir_camino(padres, destino)
            out = " -> ".join(recorrido)
            print(out)
            print("Costo: " + str(orden[destino]))

def todos_en_rango(g, articulo, rango, articulos):
    if articulo not in articulos:
        print (ART_INV)
    else: 
        padres, orden = biblioteca.bfs(g, articulo)
        cont = 0
        for o in orden.values():
            if o == int(rango):
                cont += 1
        print(cont)

def diametro(g):
    diametro_max = 0
    padres_res = {}
    fin = ""
    for v in g.obtener_vertices():
        padres, orden = biblioteca.bfs(g, v)
        max_orden = 0
        item_max = ""
        for item, ord in orden.items():
            if ord > max_orden:
                max_orden = ord
                item_max = item
        if max_orden > diametro_max:
            diametro_max = max_orden
            padres_res = padres
            fin = item_max
    recorrido = biblioteca.reconstruir_camino(padres_res, fin)
    out = " -> ".join(recorrido)
    print(out)
    print (diametro_max)

def navegacion_primer_link(g, origen, articulos):
    if origen not in articulos:
        print(PAG_404)
    else:
        l = []
        cont = 0
        for i in range (LIM_ARTICULOS):
            l.append(origen)
            ad = g.adyacentes(origen)
            if len(ad) == 0:
                break
            origen = ad[0]
        out = " -> ".join(l)
        print(out)


def clustering(g, origen, articulos):
    if origen != None and origen not in articulos:
        print(PAG_404)
    else:
        cont = 0
        if origen != None:
            res = clustering_aux(g, origen)
            print (cluster_print(res))
        else:
            aristas = {}
            for v in g.obtener_vertices():
                cont += float(clustering_aux(g, v, aristas))
            res = (1/len(g.obtener_vertices())) * cont
            print (cluster_print(res))

def cluster_print(res):
    res = str(round(float(res), 3))
    while len(res) < 5:
        res += "0"
    return res


def clustering_aux(g, origen, aristas={}):
    ads = g.adyacentes(origen)
    res = 0
    cont = 0
    if len (ads) > 1:
        for w in ads:
            for u in ads:
                if w != u and u != origen and g.estan_unidos(w,u):
                    cont += 1
        res = cont/(len(ads)*(len(ads)-1))
    return (res)

def lectura_2am(g, arts, articulos):
    nuevo_g = grafo.Grafo(True)
    for art in arts:
        if not art in articulos:
            print ("No se pudo encontrar uno de los artículos")
            break
        nuevo_g.agregar_vertice(art)
    if len(nuevo_g.obtener_vertices()) == len(arts):
        for art in nuevo_g.obtener_vertices():
            for w in g.adyacentes(art):
                if w in arts:
                    nuevo_g.agregar_arista(w, art)
        res = []
        try:
            res = biblioteca.topologico_grados(nuevo_g)
        except ValueError:
            print("No existe forma de leer las paginas en orden")
        if len(res) != 0:
            res = ", ".join(res)
            print(res)




