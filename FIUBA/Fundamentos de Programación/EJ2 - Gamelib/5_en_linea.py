import gamelib

DIM_GRILLA = 1 #esta constante define el tamaño que va a tener nuestro juego. Cambiar de valor este constante no debería romper la lógica del juego, siempre y cuando sea mayor a 0. Esto nos permite jugar, por ejemplo, un ta te ti
ANCHO_VENTANA = 350
ALTO_VENTANA = 400
ANCHO_CELDA = ((ANCHO_VENTANA - 50) // DIM_GRILLA) #se le restan a ANCHO_VENTANA y a ALTO_VENTANA la cantidad de pixeles que corresponden a los márgenes en x e y, para reflejar el valor de cada celda
ALTO_CELDA = ((ALTO_VENTANA - 100) // DIM_GRILLA)


def juego_crear():
    """Inicializar el estado del juego"""
    juego = []
    cant_columnas = []
    for i in range (DIM_GRILLA): #hacerlo asi te permite cambiar la dimension de toda la grilla, cambiando la constante DIM_GRILLA
        cant_columnas.append(" ")
    for i in range (DIM_GRILLA):
        juego.append(cant_columnas.copy())
    juego.append("X") #la idea es que la anteúltima posicion de juego corresponda al turno que se acaba de jugar, para poder accederlo desde las otras funciones
    juego.append("O") #la ultima posicion corresponde al turno actual, para poder mostrarlo por pantalla

    return juego


def juego_actualizar(juego, x, y):
    """Actualizar el estado del juego

    x e y son las coordenadas (en pixels) donde el usuario hizo click.
    Esta función determina si esas coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    j = (x - 25) // ANCHO_CELDA #se le restan, a x e y, los píxeles correspondientes a los márgenes izquierdos y superiores, para que el valor de j e i queden centrados con la grilla
    i = (y - 50) // ALTO_CELDA
    
    if j >= 0 and j <= len(juego[:-3]) and i >= 0 and i <= len(juego[:-3]) and juego[i][j] == " ": #se verifica que se haya clickeado adentro de los límites de la grilla, y en una celda vacía
        if juego[-2] == "O": #lógica para cambiar de turno. También actualiza el turno siguiente. En vez de usar los indices 10 y 11, uso el -2 y -1 para permitir el cambio de grilla sin romper la logica
            juego[-2] = "X"
            juego[-1] = "O"
        else:
            juego[-2] = "O"
            juego[-1] = "X"
        juego[i][j] = juego[-2]
    return juego

def juego_mostrar(juego):
    """Actualizar la ventana"""

    gamelib.draw_text('5 en línea', 175, 20)
    gamelib.draw_text('Turno: ' + str(juego[-1]), 175, 375)
    for n in range (25,325,ANCHO_CELDA):
        for i in range (50,350,ALTO_CELDA):
            gamelib.draw_rectangle(n, i, n + ANCHO_CELDA, i + ALTO_CELDA, outline='white', fill="")
    for fila in range (len(juego[:-2])):
        for columna in range (len(juego[fila])):
                x = (columna * ANCHO_CELDA) + 25 + (ANCHO_CELDA // 2) #a la conversion de coordenadas a pixeles, se le suma lo correspondiente al margen, y la mitad de la longitud de una celda para que quede centrado
                y = (fila * ALTO_CELDA) + 50 + (ALTO_CELDA // 2)
                gamelib.draw_text(juego[fila][columna], x, y, size = ALTO_CELDA // 2) #el tamaño está pensado para que se adecue a la dimension del juego que hayamos elegido
 



def main():
    juego = juego_crear()

    # Ajustar el tamaño de la ventana
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)

    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        gamelib.draw_begin()
        juego_mostrar(juego)
        gamelib.draw_end()

        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()

        if not ev:
            # El usuario cerró la ventana.
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            juego = juego_actualizar(juego, x, y)

gamelib.init(main)
