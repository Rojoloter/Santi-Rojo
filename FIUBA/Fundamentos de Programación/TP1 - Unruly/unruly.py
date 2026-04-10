"""Lógica del juego Unruly"""
from typing import List, Tuple, Any

Grilla = Any


def crear_grilla(desc: List[str]) -> Grilla:
    """Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Se puede asumir que la cantidad de las
    filas y columnas son múltiplo de dos. **No** se puede asumir que la
    cantidad de filas y columnas son las mismas.
    Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
         ' '  Vacío
         '1'  Casillero ocupado por un 1
         '0'  Casillero ocupado por un 0

    Ejemplo:

    >>> crear_grilla([
        '  1 1 ',
        '  1   ',
        ' 1  1 ',
        '  1  0',
    ])
    """
    Grilla = desc.copy() 
    return Grilla
    #Sé que conviene hacer una lista de listas, pero entendí mal el uso de esta función (pensé que era la encargada de formar la grilla en la terminal con prints)
    #e hice todo el resto de funciones pensando en una lista de cadenas.
    #Cuando me di cuenta del uso de esta función, era más dificil modificar el resto de funciones para que tomen una lista de listas, que dejarlo como una lista de cadenas



def dimensiones(grilla: Grilla) -> Tuple[int, int]:
    """Devuelve la cantidad de columnas y la cantidad de filas de la grilla
    respectivamente (ancho, alto)"""
    return len(grilla[0]), len(grilla)


def posicion_es_vacia(grilla: Grilla, col: int, fil: int) -> bool:
    """Devuelve un booleano indicando si la posición de la grilla dada por las
    coordenadas `col` y `fil` está vacía"""
    return grilla[fil][col] == " "

def posicion_hay_uno(grilla: Grilla, col: int, fil: int) -> bool:
    """Devuelve un booleano indicando si la posición de la grilla dada por las
    coordenadas `col` y `fil` está el valor 1"""
    return grilla[fil][col] == "1"


def posicion_hay_cero(grilla: Grilla, col: int, fil: int) -> bool:
    """Devuelve un booleano indicando si la posición de la grilla dada por las
    coordenadas `col` y `fil` está el valor 0"""
    return grilla[fil][col] == "0"


def cambiar_valor(grilla: Grilla, col: int, fil: int, valor: Any):
    """Modifica la grilla, colocando cualquier valor en la posición de la grilla
    dada por las coordenadas `col` y `fil`. Evita repetir código en las funciones
    cambiar_a_uno, cambiar_a_cero y cambiar_a_vacio"""
    cadena_reemplazo = grilla[fil][:col] + str(valor) + grilla[fil][col + 1:]
    grilla.pop(fil)
    grilla.insert(fil, cadena_reemplazo)
    return grilla



def cambiar_a_uno(grilla: Grilla, col: int, fil: int):
    """Modifica la grilla, colocando el valor 1 en la posición de la grilla
    dada por las coordenadas `col` y `fil`"""
    cambiar_valor(grilla, col, fil, 1)
    return grilla


def cambiar_a_cero(grilla: Grilla, col: int, fil: int):
    """Modifica la grilla, colocando el valor 0 en la posición de la grilla
    dada por las coordenadas `col` y `fil`"""
    cambiar_valor(grilla, col, fil, 0)
    return grilla


def cambiar_a_vacio(grilla: Grilla, col: int, fil: int):
    """Modifica la grilla, eliminando el valor de la posición de la grilla
    dada por las coordenadas `col` y `fil`"""
    cambiar_valor(grilla, col, fil, " ")
    return grilla

def fila_es_valida(grilla: Grilla, fil: int) -> bool:
    """Devuelve un booleano indicando si la fila de la grilla denotada por el
    índice `fil` es considerada válida.

    Una fila válida cuando se cumplen todas estas condiciones:
        - La fila no tiene vacíos
        - La fila tiene la misma cantidad de unos y ceros
        - La fila no contiene tres casilleros consecutivos del mismo valor
    """
    fila_analizada_str = "".join(grilla[fil])
    contador_de_1 = fila_analizada_str.count("1")
    contador_de_0 = fila_analizada_str.count("0")
    if contador_de_0 == contador_de_1:
        if " " not in fila_analizada_str:
            if  "111" not in fila_analizada_str and "000" not in fila_analizada_str:
                return True
    return False



def columna_es_valida(grilla: Grilla, col: int) -> bool:
    """Devuelve un booleano indicando si la columna de la grilla denotada por
    el índice `col` es considerada válida.

    Las condiciones para que una columna sea válida son las mismas que las
    condiciones de las filas."""
    columna_analizada = ""
    for i in range (len(grilla)):
        columna_analizada += grilla[i][col]
    
    contador_de_1 = columna_analizada.count("1")
    contador_de_0 = columna_analizada.count("0")
    if contador_de_0 == contador_de_1:
        if " " not in columna_analizada:
            if  "111" not in columna_analizada and "000" not in columna_analizada:
                return True
    return False




def grilla_terminada(grilla: Grilla) -> bool:
    """Devuelve un booleano indicando si la grilla se encuentra terminada.

    Una grilla se considera terminada si todas sus filas y columnas son
    válidas."""
    
    for i in range (len(grilla)):
        if fila_es_valida(grilla, i) != True:
            return False

    for i in range (len(grilla[0])):
        if columna_es_valida(grilla, i) != True:
            return False

    return True