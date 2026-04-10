import gamelib
import copy
import png

ANCHO_VENTANA = 700
#El mínimo valor de ANCHO_VENTANA es 220. De otro modo, la paleta de colores se empieza a solapar. 
#Sin embargo, aunque sigue funcionando, se torna dificil leer el texto dentro de los botones superiores con una resolución tan baja. Por eso se recomienda una resolución minima de 500 pixeles
ALTO_VENTANA = 800
#ALTO_VENTANA no puede ser inferior a ANCHO_VENTANA(sí puede ser igual) porque los elementos de la interfaz se muestran de forma horizontal


MARGEN_HORIZONTAL_PAINT = 50
MARGEN_VERTICAL_PAINT = 50 + (ALTO_VENTANA -  ANCHO_VENTANA) // 2

DIMENSION_PAINT_DEFAULT = 20
TAMAÑO_PIXEL_DEFAULT = (ANCHO_VENTANA - MARGEN_HORIZONTAL_PAINT * 2) // DIMENSION_PAINT_DEFAULT
PIXELES_PAINT = TAMAÑO_PIXEL_DEFAULT * DIMENSION_PAINT_DEFAULT

PIXEL_COLORES = TAMAÑO_PIXEL_DEFAULT + 5
MARGEN_COLORES = 5
ALTURA_COLORES = PIXELES_PAINT + MARGEN_VERTICAL_PAINT + MARGEN_COLORES
SEPARACION_ENTRE_COLORES = 5
MARGEN_COLOR_ARBITRARIO = min(ANCHO_VENTANA, ALTO_VENTANA) - MARGEN_HORIZONTAL_PAINT - PIXEL_COLORES

ALTURA_INFERIOR_BOTON = MARGEN_VERTICAL_PAINT - 5
ALTURA_SUPERIOR_BOTON = ALTURA_INFERIOR_BOTON - 35
ANCHO_BOTON = TAMAÑO_PIXEL_DEFAULT * 3
MARGEN_BOTON = TAMAÑO_PIXEL_DEFAULT

COLORES = ("white", "black", "red", "green", "blue", "cyan", "yellow")

def definir_dimensiones_iniciales():
    """pregunta al usuario por las dimensiones iniciales del paint. Si el input es invalido, usa unas dimensiones default"""
    tamaño_paint = gamelib.input("ingrese la cantidad de pixeles del ancho y del alto del paint separado por una coma")
   
    if tamaño_paint == None:
        gamelib.say("Usando valores predeterminados")
        ancho_paint, alto_paint = (DIMENSION_PAINT_DEFAULT, DIMENSION_PAINT_DEFAULT)

    elif "," in tamaño_paint and len(tamaño_paint.split(",")) == 2 and ("".join(tamaño_paint.split(","))).isdigit() and int(tamaño_paint.split(",")[0]) > 0  and int(tamaño_paint.split(",")[1]) > 0:
        ancho_paint, alto_paint = tamaño_paint.split(",")
    else: 
        gamelib.say("Valores ingresados no válidos, usando valores predeterminados")
        ancho_paint, alto_paint = (DIMENSION_PAINT_DEFAULT, DIMENSION_PAINT_DEFAULT)

    return (int(ancho_paint), int(alto_paint))

def paint_nuevo(dimensiones):
    '''inicializa el estado del programa con una imagen vacía de ancho x alto pixels'''
    ancho_paint, alto_paint = dimensiones
    grilla = []
    filas = []
    
    for i in range (int(ancho_paint)):
        filas.append("white")
    for i in range (int(alto_paint)):
        grilla.append(filas.copy())
    
    return {"paint": grilla, "color_actual": "white", "color_arbitrario": "#FFFFFF", "ancho_paint": int(ancho_paint), "alto_paint": int(alto_paint), "dimension_pixel": PIXELES_PAINT // max(int(ancho_paint), int(alto_paint)), "margen_ancho": MARGEN_HORIZONTAL_PAINT, "margen_alto": MARGEN_VERTICAL_PAINT, "click_activo": False}
    #El color arbitrario está en Hexadecimal para que no se interprete que están tanto el blanco como el color arbitrario seleccionados al iniciar el programa.
    #click_activo nos sirve para poder dibujar mientras mantenemos apretado el click izquierdo
    #el resto es el paint, e información del mismo (dimensiones, dimensiones de los pixeles, etc)


def mostrar_paleta(paint):
    """Muestra en pantalla la paleta de colores, y un color a elección"""
    
    sangria = MARGEN_HORIZONTAL_PAINT
    
    for i in COLORES: #para colores predefinidos
        if not i == paint["color_actual"]:
            gamelib.draw_rectangle(sangria, ALTURA_COLORES, sangria + PIXEL_COLORES, ALTURA_COLORES + PIXEL_COLORES, outline='gray', fill=i, width = 1) #los que no estan seleccionados
        else: gamelib.draw_rectangle(sangria, ALTURA_COLORES, sangria + PIXEL_COLORES, ALTURA_COLORES + PIXEL_COLORES, outline='gray', fill=i, width = 5) #el color seleccionado
        sangria += PIXEL_COLORES + SEPARACION_ENTRE_COLORES

    if paint["color_actual"] == paint["color_arbitrario"]: #revisa si esta seleccionado el color arbitrario
        gamelib.draw_rectangle(MARGEN_COLOR_ARBITRARIO, ALTURA_COLORES, MARGEN_COLOR_ARBITRARIO + PIXEL_COLORES, ALTURA_COLORES + PIXEL_COLORES, outline='gray', fill=paint["color_arbitrario"], width = 5)
    else: gamelib.draw_rectangle(MARGEN_COLOR_ARBITRARIO, ALTURA_COLORES, MARGEN_COLOR_ARBITRARIO + PIXEL_COLORES, ALTURA_COLORES + PIXEL_COLORES, outline='gray', fill=paint["color_arbitrario"], width = 1)
    gamelib.draw_text("Color a elección", MARGEN_COLOR_ARBITRARIO + PIXEL_COLORES//2, ALTURA_COLORES + PIXEL_COLORES + 10) #El 15 es para que no esté pegado a la parte inferior del color



def seleccionar_colores(paint, x, y):
    """Permite cambiar el color actual y el color a elección dentro de la lógica del programa"""
    
    j = (x - MARGEN_HORIZONTAL_PAINT) // (PIXEL_COLORES + SEPARACION_ENTRE_COLORES)
    k = (y - ALTURA_COLORES) // PIXEL_COLORES
    
    if j >= 0 and j <= 6 and k == 0: #para seleccionar un color predefinido
        paint["color_actual"] = COLORES[j]
    
    j = (x - MARGEN_COLOR_ARBITRARIO) // (PIXEL_COLORES)

    if j == 0 and k == 0: #logica para cambiar de color el color arbitrario
        input_RGB = gamelib.input ("Ingrese un color mediante sintaxis #rrggbb (0-255, 0-255, 0-255). OK sin ingresar nada selecciona el color a elección actual")
        if input_RGB != None: #Este sería el caso en el que apretamos "Cancel"
            if "," in input_RGB:
                valor_RGB = input_RGB.split(",")
                if len(valor_RGB) == 3 and "".join(valor_RGB).isdigit() and int(valor_RGB[0]) >= 0 and int(valor_RGB[0]) <= 255 and int(valor_RGB[1]) >= 0 and int(valor_RGB[1]) <= 255 and int(valor_RGB[2]) >= 0 and int(valor_RGB[2]) <= 255:
                    color_RGB = f'{int(valor_RGB[0]):02x}' + f'{int(valor_RGB[1]):02x}' + f'{int(valor_RGB[2]):02x}'
                    paint["color_arbitrario"] = "#" + color_RGB
                    paint["color_actual"] = paint["color_arbitrario"]
                else: gamelib.say("Lo que ha ingresado no sigue el formato #RRGGBB")
            elif len(input_RGB) == 0:
                paint["color_actual"] = paint["color_arbitrario"]
            else: gamelib.say("Lo que ha ingresado no sigue el formato #RRGGBB")



def cambiar_colores_paint (paint, x, y):
    """Modifica los colores de los pixeles"""

    j = (y - paint["margen_alto"]) // paint["dimension_pixel"]
    k = (x - paint["margen_ancho"]) // paint["dimension_pixel"]

    if j >= 0 and j <= len(paint["paint"]) - 1 and k >= 0 and k <= len(paint["paint"][0]) - 1:
        paint["paint"][j][k] = paint["color_actual"]




def paint_mostrar_imagen(paint):
    '''muestra la imagen en pantalla''' #Decidí no incluir en esta función, la parte encargada de mostrar la paleta de colores. Me pareció más ordenado 
    offset_vertical = 0
    offset_horizontal = 0
    if paint["ancho_paint"] > paint["alto_paint"]:
        offset_vertical = (paint["ancho_paint"] - paint["alto_paint"])
    elif paint["ancho_paint"] < paint["alto_paint"]:
        offset_horizontal = (paint["alto_paint"] - paint["ancho_paint"])
    
    paint["margen_alto"] = MARGEN_VERTICAL_PAINT + offset_vertical * paint["dimension_pixel"] // 2
    paint["margen_ancho"] = MARGEN_HORIZONTAL_PAINT + offset_horizontal * paint["dimension_pixel"] // 2
    
    for n in range (paint["margen_ancho"], paint["margen_ancho"] + paint["ancho_paint"] * paint["dimension_pixel"], paint["dimension_pixel"]):
        for i in range (paint["margen_alto"], paint["margen_alto"] + paint["alto_paint"] * paint["dimension_pixel"], paint["dimension_pixel"]):
            gamelib.draw_rectangle(n, i, n + paint["dimension_pixel"], i + paint["dimension_pixel"], outline='black', fill=paint["paint"][(i-(paint["margen_alto"]))//paint["dimension_pixel"]][(n-(paint["margen_ancho"]))//paint["dimension_pixel"]])
    


def mostrar_botones_archivos():
    """muestra por pantalla los botones para exportar ppm, exportar png e importar ppm"""
    
    gamelib.draw_rectangle(ANCHO_VENTANA - MARGEN_HORIZONTAL_PAINT - ANCHO_BOTON, ALTURA_SUPERIOR_BOTON, min(ANCHO_VENTANA, ALTO_VENTANA) - MARGEN_HORIZONTAL_PAINT, ALTURA_INFERIOR_BOTON) #Importar PPM.
    gamelib.draw_text("IMPORTAR PPM", ANCHO_VENTANA - MARGEN_HORIZONTAL_PAINT - ANCHO_BOTON // 2, (ALTURA_INFERIOR_BOTON + ALTURA_SUPERIOR_BOTON) // 2, bold=True, size=ANCHO_BOTON // 10, fill="black")

    gamelib.draw_rectangle(MARGEN_HORIZONTAL_PAINT, ALTURA_SUPERIOR_BOTON, MARGEN_HORIZONTAL_PAINT + ANCHO_BOTON, ALTURA_INFERIOR_BOTON) #Exportar PPM.
    gamelib.draw_text("EXPORTAR PPM", MARGEN_HORIZONTAL_PAINT + ANCHO_BOTON // 2, (ALTURA_INFERIOR_BOTON + ALTURA_SUPERIOR_BOTON) // 2, bold=True, size=ANCHO_BOTON // 10, fill="black")

    gamelib.draw_rectangle(MARGEN_HORIZONTAL_PAINT + ANCHO_BOTON + MARGEN_BOTON, ALTURA_SUPERIOR_BOTON, MARGEN_HORIZONTAL_PAINT + ANCHO_BOTON + MARGEN_BOTON + ANCHO_BOTON, ALTURA_INFERIOR_BOTON) #Exportar PNG.
    gamelib.draw_text("EXPORTAR PNG", MARGEN_HORIZONTAL_PAINT + ANCHO_BOTON + MARGEN_BOTON + ANCHO_BOTON // 2, (ALTURA_INFERIOR_BOTON + ALTURA_SUPERIOR_BOTON) // 2, bold=True, size=ANCHO_BOTON // 10, fill="black")

    


def importar_ppm():
    """modifica el estado inicial con la informacion de pixeles del archivo ppm"""
    
    importar_ppm = gamelib.input("Ingrese la ruta completa para importar su archivo PPM")    
    
    if importar_ppm != None:
        try:
            if len(importar_ppm) > 0 and "." in importar_ppm:
                
                if (importar_ppm.split("."))[1] != "ppm":
                    gamelib.say("El archivo debe tener una extensión PPM")
                    return None
            else:
                gamelib.say("El archivo debe tener una extensión PPM")
                return None

            with open (importar_ppm) as ppm:

                encabezado = (ppm.readline()).rstrip()
                if encabezado != "P3":
                    gamelib.say("El encabezado del archivo PPM no es válido")
                    return None
                dimensiones = ((ppm.readline()).rstrip()).split()
                if len(dimensiones) == 2 and dimensiones[0].isdigit() and dimensiones[1].isdigit():
                    ancho, alto = dimensiones
                else:
                    gamelib.say("Las dimensiones del archivo PPM no son validas")
                    return None
                dimension_paint_ppm = (int(ancho), int(alto))
                
                paint_ppm = paint_nuevo(dimension_paint_ppm)

                max_intensidad = (ppm.readline())

                for i in range (paint_ppm["alto_paint"]):
                    info_fila = (ppm.readline()).split()
                    for j in range (paint_ppm["ancho_paint"]):
                        paint_ppm["paint"][i][j] = "#" + f'{int(info_fila[0]):02x}' + f'{int(info_fila[1]):02x}' + f'{int(info_fila[2]):02x}'
                        info_fila = info_fila[3:]
            
            return paint_ppm
        except FileNotFoundError:
            gamelib.say("El archivo que ha ingresado no existe")
        except PermissionError:
            gamelib.say("El programa no tiene permisos para leer este archivo")
    
    return None



def color_a_hexadecimal(paint):
    """Cambia los valores de los colores de su forma común a su forma hexadecimal""" 
    #Hago el cambio acá en vez de hacer todo directamente en hexadecimal, porque la distinción es importante en la función mostrar_paleta 

    color_a_hex = {"white": "#FFFFFF", "black": "#000000", "red": "#FF0000", "green": "#008000", "blue": "#0000FF", "cyan": "#00FFFF", "yellow": "#FFFF00"}
    for i in range (len(paint["paint"])):
        for j in range (len(paint["paint"][i])):
            if paint["paint"][i][j] in color_a_hex:
                paint["paint"][i][j] = color_a_hex[paint["paint"][i][j]]


def exportar_ppm(paint, x, y):
    """permite exportar la imagen dibujada en el paint con formato ppm"""

    if x >= MARGEN_HORIZONTAL_PAINT and x <= MARGEN_HORIZONTAL_PAINT + ANCHO_BOTON and y >= ALTURA_SUPERIOR_BOTON and y <= ALTURA_INFERIOR_BOTON:
        ruta_destino = gamelib.input("Ingrese la ruta completa para guardar su archivo PPM")
        
        if ruta_destino != None:
            if len(ruta_destino) > 0 and "." in ruta_destino:
                if (ruta_destino.split("."))[1] != "ppm":
                    gamelib.say("El archivo debe tener una extensión PPM")
                    return None
            else: 
                gamelib.say("El archivo debe tener una extensión PPM")
                return None
            
            try:
                with open (ruta_destino, "w") as ppm:
                    ppm.write("P3\n") #Encabezado
                    ppm.write(f'{paint["ancho_paint"]} {paint["alto_paint"]}\n') #Dimensiones
                    ppm.write("255\n") #La maxima intensidad, siempre es 255
                    color_a_hexadecimal(paint)
                
                    for fila in paint["paint"]:
                        lista_fila_aux = []
                        for color in fila:
                            for caracter in color:
                                lista_fila_aux.append(caracter)
                            
                            while "#" in  lista_fila_aux: #uso un while porque la funcion remove solo elimina el primer elemento que encuentra que coincide con el parametro. Así me aseguro que se borran todos los "#"
                                lista_fila_aux.remove("#")

                        for i in range(0, len(lista_fila_aux), 2):
                            ppm.write(f'{str(int("".join(lista_fila_aux[i: i+2]), 16))} ')
                        ppm.write("\n")
            except PermissionError:
                gamelib.say("El programa no tiene permisos para leer este archivo")

def exportar_png(paint, x, y):
    """permite exportar la imagen dibujada en el paint con formato png"""
    
    if x >= MARGEN_HORIZONTAL_PAINT + ANCHO_BOTON + MARGEN_BOTON and x <= MARGEN_HORIZONTAL_PAINT + ANCHO_BOTON + MARGEN_BOTON + ANCHO_BOTON and y >= ALTURA_SUPERIOR_BOTON and y <= ALTURA_INFERIOR_BOTON:
        diccionario_colores = {}
        lista_paleta = []
        color_a_hexadecimal(paint)
        paint_png = copy.deepcopy(paint)

        for fila in paint_png["paint"]:
            colores_fila = ("".join(fila)).split("#")
            colores_fila.pop(0)
            for color in colores_fila:
                diccionario_colores[f"#{color}"] = (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))
        
        for color_dec in diccionario_colores.values():
            lista_paleta.append(color_dec)
        
        for i in range (paint_png["alto_paint"]):
            for j in range (paint_png["ancho_paint"]):
                if paint_png["paint"][i][j] in diccionario_colores:
                    paint_png["paint"][i][j] = diccionario_colores[paint_png["paint"][i][j]]
                paint_png["paint"][i][j] = lista_paleta.index(paint_png["paint"][i][j])
        
        imagen = []
        for fila in paint_png["paint"]:
            imagen.append(fila)     
        
        ruta_png = gamelib.input("Ingrese la ruta donde quiere guardar su archivo PNG")
        if ruta_png != None:
            
            if len(ruta_png) > 0 and "." in ruta_png:
                if (ruta_png.split("."))[1] != "png":
                    gamelib.say("El archivo debe tener una extensión PNG")
                    return None
            else: 
                gamelib.say("El archivo debe tener una extensión PNG")
                return None
        
        
            try:
                png.escribir(ruta_png, lista_paleta, imagen)
            except PermissionError:
                gamelib.say("El programa no tiene permisos para leer este archivo")
        
        

def main():
    gamelib.title("AlgoPaint")
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    
    dimensiones_iniciales = definir_dimensiones_iniciales()
    paint = paint_nuevo(dimensiones_iniciales)
    while gamelib.loop(fps=15):
        
        gamelib.draw_begin()
        
        paint_mostrar_imagen(paint)
        mostrar_paleta(paint)
        mostrar_botones_archivos()
        
        gamelib.draw_end()

        for ev in gamelib.get_events():
            
            if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
                
                seleccionar_colores(paint, ev.x, ev.y)
                cambiar_colores_paint (paint, ev.x, ev.y)
                exportar_ppm(paint, ev.x, ev.y)
                exportar_png(paint, ev.x, ev.y)
                

                if ev.x >= paint["margen_ancho"] and ev.x <= paint["margen_ancho"] + paint["ancho_paint"] * paint["dimension_pixel"] and ev.y >= paint["margen_alto"] and ev.y <= paint["margen_alto"] + paint["alto_paint"] * paint["dimension_pixel"]:
                    #Lo restrinjo nada más al lienzo porque hay un bug al momento de seleccionar el color a eleccion.
                    #Al presionarlo, sale un mensaje pidiendo un input, y esto parece que restringe el hecho de que el click izquierdo dejó de ser presionado.
                    #Esto hace que el programa siga pintando aunque el usuario no esté haciendo click.
                    #Por eso me pareció mas conveniente restringirlo en vez de intentar arreglar ese error
                    paint["click_activo"] = True
                
                if ev.x >= ANCHO_VENTANA - MARGEN_HORIZONTAL_PAINT - ANCHO_BOTON and ev.x <= ANCHO_VENTANA - MARGEN_HORIZONTAL_PAINT and ev.y >= ALTURA_SUPERIOR_BOTON and ev.y <= ALTURA_INFERIOR_BOTON:
                    paint_importar_ppm = importar_ppm()
                    if paint_importar_ppm != None:
                        paint = paint_importar_ppm
            
            if paint["click_activo"] == True and ev.type == gamelib.EventType.Motion:
                cambiar_colores_paint (paint, ev.x, ev.y)
            
            elif ev.type == gamelib.EventType.ButtonRelease and ev.mouse_button == 1:
                paint["click_activo"] = False


gamelib.init(main)