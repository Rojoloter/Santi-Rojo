def leer_ofertas(nombre_archivo):
    nombres = []
    ofertas = []
    with open(nombre_archivo, "r") as f:
        m = int(f.readline().strip())
        for linea in f:
            partes = [x.strip() for x in linea.strip().split(",") if x.strip()]
            nombre = partes[0]
            valores = [int(x) for x in partes[1:]]
            nombres.append(nombre)
            ofertas.append(valores)
    return m, nombres, ofertas


def leer_restricciones(nombre_archivo, nombres):
    restricciones = [set() for _ in nombres]
    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue
            nombres_incompatibles = [nombre.strip() for nombre in linea.strip().split(',') if nombre.strip()]
            indices = [nombres.index(nombre) for nombre in nombres_incompatibles]
            principal = indices[0]
            restricciones[principal].update(indices[1:])
    return restricciones