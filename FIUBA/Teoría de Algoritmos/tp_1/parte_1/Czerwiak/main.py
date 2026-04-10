import sys

def apilarMonedas(monedas):
    pilas = []
    pilas.append([monedas[0]])

    for i in range(1,len(monedas)):
        apilado = False
        for pila in pilas:
            if(pila[len(pila) -1] > monedas[i]):
                pila.append(monedas[i])
                apilado = True 
                break  
        if(not apilado):
            pilas.append([monedas[i]])        
            
    print(len(pilas))

def leer_monedas(archivo):
    monedas_a_leer = open(archivo, 'r')
    monedas = []
    for moneda in monedas_a_leer.readlines():
        monedas.append(int(moneda))

    return monedas

def main(archivo):
    try: 
        monedas = leer_monedas(archivo)
        apilarMonedas(monedas)
    except: 
        print("No se pudo leer el archivo.")
    return 0

if __name__ == "__main__":
    if(len(sys.argv)<=1):
        print("Debe ejecutar enviando el archivo de monedas luego de main.py")
    else:
        archivo = sys.argv[1]
        main(archivo)
    
