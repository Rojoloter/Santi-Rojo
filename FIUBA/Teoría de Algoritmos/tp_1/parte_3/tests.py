import unittest

from puentes_pd import buscar_posicion

import itertools

def reconstruccion(max, prev, secuencia):
    # Reconstrucción de la subsecuencia más larga
    max_sub_sequencia = []
    
    index = max
    while index != -1:
        max_sub_sequencia.append(secuencia[index])
        index = prev[index]

    # La subsecuencia está en orden inverso
    max_sub_sequencia.reverse()
    
    return max_sub_sequencia

def secuencia_creciente_mas_larga1(secuencia: list[int]) -> list[int]:
    if len(secuencia) == 0:
        return []
    sub_secuencia = []
    # Arreglo para reconstruir la subsecuencia
    prev = [-1] * len(secuencia)
    indices = [-1] * len(secuencia)
    for i, num in enumerate(secuencia):
        # Encontramos la posición donde insertar 'num' de manera que la lista siga ordenada
        pos = buscar_posicion(sub_secuencia, num)
        # Si 'num' es mayor que todos los elementos en 'sub_secuencia', lo agregamos al final
        if pos == len(sub_secuencia):
            sub_secuencia.append(num)
        else:
            sub_secuencia[pos] = num

        indices[pos] = i
        # Si pos > 0, significa que existe un elemento antes de 'num' en la subsecuencia
        if pos > 0:
            prev[i] = indices[pos - 1]
            
    max = indices[len(sub_secuencia) - 1]

    return reconstruccion(max, prev, secuencia)

def secuencia_creciente_mas_larga2(secuencia: list[int]) -> list[int]:
    if len(secuencia) == 0:
        return []
    sub_secuencia = []
    # Arreglo para reconstruir la subsecuencia
    prev = [-1] * len(secuencia)
    indices = [-1] * len(secuencia)
    max = -1
    for i, num in enumerate(secuencia):
        # Encontramos la posición donde insertar 'num' de manera que la lista siga ordenada
        pos = buscar_posicion(sub_secuencia, num)
        # Si 'num' es mayor que todos los elementos en 'sub_secuencia', lo agregamos al final
        if pos == len(sub_secuencia):
            sub_secuencia.append(num)
            max = i
        else:
            sub_secuencia[pos] = num
        
        indices[pos] = i
        # Si pos > 0, significa que existe un elemento antes de 'num' en la subsecuencia
        if pos > 0:
            prev[i] = indices[pos - 1]

    return reconstruccion(max, prev, secuencia)




def test():
    n = 5
    # Cambiá esto para probar con otros valores

    for k in range(1, n + 1):
        elementos = list(range(k))  # [0], [0,1], [0,1,2], ...
        for perm in itertools.permutations(elementos):
            arr = list(perm)
            resultadoA = secuencia_creciente_mas_larga1(arr)
            resultadoB = secuencia_creciente_mas_larga2(arr)
            if len(resultadoA) != len(resultadoB):
                print(f"Falla con {perm}: A={resultadoA}, B={resultadoB}")
            else:
                if (resultadoA != resultadoB):
                    print(f"OK: {perm}: A={resultadoA}, B={resultadoB}")

if __name__ == '__main__':
    test()
    """ secuencia = [2, 5, 3, 7, 11, 8, 10, 13, 6]


    print(secuencia_creciente_mas_larga1(secuencia))
    print(secuencia_creciente_mas_larga2(secuencia)) """
