
import sys

class Pila_cartas(object):
    def __init__(self):
        self.cartas = []
        self.tope :int = 0
    def diferencia_tope(self, carta_operar :int):
        return carta_operar - self.tope
    def añadir_carta(self, carta_añadiendo :int):
        self.cartas.append(carta_añadiendo)
        self.tope = carta_añadiendo 
       
def main(nombre_archivo :str):
    mazo = open(nombre_archivo, "r")
    pilas = []
    for carta in mazo:
        carta = int(carta)
        if len(pilas) >= 1:
            i = 0
            pos_apilo = -1
            while i < len(pilas):
                if pilas[i].diferencia_tope(carta) < 0:
                    pos_apilo = i
                    i = len(pilas)
                else:
                    i = i + 1
            if pos_apilo >= 0:
                pilas[pos_apilo].añadir_carta(carta)
            else:
                pilas.append(Pila_cartas())
                pilas[-1].añadir_carta(carta)
        else:
            pilas.append(Pila_cartas())
            pilas[0].añadir_carta(carta)
    print(len(pilas))
    mazo.close()

if __name__=="__main__":
    main(sys.argv[1])