from vectores import norma, diferencia, prodvect


def area_triangulo(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    """reciba las coordenadas de 3 puntos en R3 y devuelva el área del triángulo que conforman."""
    AB = diferencia(x2, y2, z2, x1, y1, z1) #AB es el vector que va desde el punto A (x1, y1, z1) al punto B (x2, y2, z2)
    ABx = AB[0] #agarro las componentes (x, y, z) por separado, ya que va a ser necesario para la funcion "prodvect" (esta funcion está esperando 6 valores)
    ABy = AB[1]
    ABz = AB[2]
    AC = diferencia(x3, y3, z3, x1, y1, z1) #AC es el vector que va desde el punto A (x1, y1, z1) al punto C (x3, y3, z3)
    ACx = AC[0] #también agarro las componentes (x, y, z)
    ACy = AC[1]
    ACz = AC[2]
    ProductoVectorial = prodvect(ABx, ABy, ABz, ACx, ACy, ACz) #Acá van los vectores AB y AC para hacer un producto vectorial
    ABACx = ProductoVectorial[0] #Vuelvo a separar este nuevo vector, resultante del producto vectorial entre AB y AC, en sus componentes (x, y, z)
    ABACy = ProductoVectorial[1]
    ABACz = ProductoVectorial[2]
    AreaABC = (norma(ABACx, ABACy, ABACz))/2 #aplicamos la formula del area, dividiendo por dos a la norma del producto vectorial entre AB y AC
    return AreaABC

print (area_triangulo(5, 8, -1, -2, 3, 4, -3, 3, 0)) #verifico que el resultado sea acorde a lo que dice el ejercicio
assert area_triangulo(1, 2, 3, 3, 2, 1, 2, 1, 3) == 1.7320508075688772
assert area_triangulo(4, 6, 6, 3, 5, 87, 2, 7, 3) == 91.26609447105754
assert area_triangulo(234, 1, -90, -43, 12, 2, -3, 9, 100) == 15429.099722602094
