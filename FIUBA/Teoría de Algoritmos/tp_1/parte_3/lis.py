def buscar_posicion(sub, num):
    izq = 0
    der = len(sub)
    while izq < der:
        medio = (izq + der) // 2
        if sub[medio] < num:
            izq = medio + 1
        else:
            der = medio
    return izq


def secuencia_creciente_mas_larga(secuencia, reverse):

    n = len(secuencia)

    # finales_minimos[i] contiene el menor final posible de una subsecuencia de longitud i+1
    finales_minimos = []
    prev = [-1] * n  # Arreglo para reconstruir la subsecuencia
    # indices[i] almacena el índice del último número de la subsecuencia de longitud i+1
    indices = [-1] * n

    orden = range(n - 1, -1, -1) if reverse else range(n)

    for i in orden:
        num = secuencia[i]
        # Encontramos la posición donde insertar 'num' de manera que la lista siga ordenada
        pos = buscar_posicion(finales_minimos, num)
        # Si 'num' es mayor que todos los elementos en 'sub_secuencia', lo agregamos al final
        if pos == len(finales_minimos):
            finales_minimos.append(num)
        else:
            finales_minimos[pos] = num

        # Si pos > 0, significa que existe un elemento antes de 'num' en la subsecuencia
        if pos > 0:
            prev[i] = indices[pos - 1]

        indices[pos] = i

    # Reconstrucción de la subsecuencia más larga
    max_sub_sequencia = []
    index = indices[len(finales_minimos) - 1]
    while index != -1:
        max_sub_sequencia.append(secuencia[index])
        index = prev[index]

    # La subsecuencia está en orden inverso
    max_sub_sequencia.reverse()

    return max_sub_sequencia


arr = [10, 9, 2, 5, 3, 7, 101, 18]
print("Con una secuencia:", arr)
resultado = secuencia_creciente_mas_larga(arr, False)
print("LIS Original:", resultado)

resultado = secuencia_creciente_mas_larga(arr, True)
print("LIS Inverso:", resultado)
