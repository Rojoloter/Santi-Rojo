package cola

type nodo[T any] struct {
	dato      T
	prox_nodo *nodo[T]
}

func crearNodo[T any](dato T) *nodo[T] {
	nuevo_nodo := new(nodo[T])
	nuevo_nodo.dato = dato
	return nuevo_nodo
}

type colaEnlazada[T any] struct {
	prim_nodo *nodo[T]
	ult_nodo  *nodo[T]
}

func CrearColaEnlazada[T any]() Cola[T] {
	cola := new(colaEnlazada[T])
	return cola
}

func (cola *colaEnlazada[T]) EstaVacia() bool {
	return cola.prim_nodo == nil && cola.ult_nodo == nil
}

func (cola *colaEnlazada[T]) Encolar(dato T) {
	nuevo_nodo := crearNodo[T](dato)

	if cola.EstaVacia() {
		cola.prim_nodo = nuevo_nodo
	} else if !cola.EstaVacia() && cola.ult_nodo == nil {
		cola.prim_nodo.prox_nodo = nuevo_nodo
		cola.ult_nodo = nuevo_nodo
	} else {
		cola.ult_nodo.prox_nodo = nuevo_nodo
	}
	cola.ult_nodo = nuevo_nodo
}

func (cola *colaEnlazada[T]) VerPrimero() T {
	if cola.EstaVacia() {
		panic("La cola esta vacia")
	}
	return cola.prim_nodo.dato
}

func (cola *colaEnlazada[T]) Desencolar() T {
	if cola.EstaVacia() {
		panic("La cola esta vacia")
	}
	dato_desencolado := cola.prim_nodo.dato
	cola.prim_nodo = cola.prim_nodo.prox_nodo
	if cola.prim_nodo == nil {
		cola.ult_nodo = nil
	}
	return dato_desencolado
}
