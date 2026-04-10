package pila

/* Definición del struct pila proporcionado por la cátedra. */

type pilaDinamica[T any] struct {
	datos    []T
	cantidad int
}

const tamaño_inicial_pila int = 10
const const_redimension int = 2
const multiplo_minimo_pila int = 4

func CrearPilaDinamica[T any]() Pila[T] {
	pila := new(pilaDinamica[T])
	pila.datos = make([]T, tamaño_inicial_pila)
	return pila
}

func (pila *pilaDinamica[T]) redimensionar(dimension int) {
	{
		nuevos_datos := make([]T, dimension)
		copy(nuevos_datos, pila.datos)
		pila.datos = nuevos_datos
	}
}

func (pila *pilaDinamica[T]) EstaVacia() bool {
	return pila.cantidad == 0
}

func (pila pilaDinamica[T]) VerTope() T {
	if pila.EstaVacia() {
		panic("La pila esta vacia")
	}
	return pila.datos[pila.cantidad-1]
}

func (pila *pilaDinamica[T]) Apilar(dato T) {
	if pila.cantidad == len(pila.datos) {
		pila.redimensionar(len(pila.datos) * const_redimension)
	}
	pila.datos[pila.cantidad] = dato
	pila.cantidad++
}

func (pila *pilaDinamica[T]) Desapilar() T {
	if pila.EstaVacia() {
		panic("La pila esta vacia")
	}
	pila.cantidad--
	if pila.cantidad*multiplo_minimo_pila <= cap(pila.datos) && cap(pila.datos) > tamaño_inicial_pila {
		pila.redimensionar(cap(pila.datos) / const_redimension)
	}
	return pila.datos[pila.cantidad]
}
