from sys import argv

def apilar(cartas):
    pilas = [] # Contiene cartas superiores de cada pila

    for carta in cartas:
        # Buscamos la primera pila en la que podemos poner la carta
        # Las pilas estan y quedan ordenadas de con su "Tope" de menor a mayor
        # Se hace una Busqueda Binaria de la primera pila valida
        izq = 0
        der = len(pilas)
        while izq < der:
            medio = (izq + der) // 2
            if pilas[medio] > carta:
                der = medio
            else:
                izq = medio + 1
        
        if izq < len(pilas): # Se encontro una pila valida
            pilas[izq] = carta
        else:   # No se pudo colocar en las pilas existentes
            pilas.append(carta) # Se coloca en una pila nueva

    return pilas

def main(argv):

    if len(argv) != 2:  
        print("Uso: python main.py archivo.txt")
        return 1
    
    with open(argv[1]) as file:
        cartas = [int(line.strip()) for line in file.readlines()]

    pilas = apilar(cartas)
    print(len(pilas))

if __name__ == "__main__":
    main(argv)