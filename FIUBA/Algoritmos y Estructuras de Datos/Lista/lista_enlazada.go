package lista

const lista_vacia = "La lista esta vacia"
const iterador_vacio = "El iterador termino de iterar"

type nodoLista[T any] struct {
	dato      T
	siguiente *nodoLista[T]
}

func crearNodo[T any](dato T) *nodoLista[T] {
	nuevo_nodo := new(nodoLista[T])
	nuevo_nodo.dato = dato
	return nuevo_nodo
}

type listaEnlazada[T any] struct {
	primero *nodoLista[T]
	ultimo  *nodoLista[T]
	largo   int
}

func CrearListaEnlazada[T any]() Lista[T] {
	lista := new(listaEnlazada[T])
	return lista
}

func (lista *listaEnlazada[T]) EstaVacia() bool {
	return lista.largo == 0
}

func (lista *listaEnlazada[T]) VerPrimero() T {
	if lista.EstaVacia() {
		panic(lista_vacia)
	}
	return lista.primero.dato
}

func (lista *listaEnlazada[T]) VerUltimo() T {
	if lista.EstaVacia() {
		panic(lista_vacia)
	}
	return lista.ultimo.dato
}

func (lista *listaEnlazada[T]) Largo() int {
	return lista.largo
}

func (lista *listaEnlazada[T]) InsertarPrimero(dato T) {
	nuevo_nodo := crearNodo[T](dato)
	nuevo_nodo.siguiente = lista.primero
	lista.primero = nuevo_nodo
	if lista.EstaVacia() {
		lista.ultimo = nuevo_nodo
	}
	lista.largo++
}

func (lista *listaEnlazada[T]) InsertarUltimo(dato T) {
	nuevo_nodo := crearNodo[T](dato)
	if lista.EstaVacia() {
		lista.primero = nuevo_nodo
		lista.ultimo = lista.primero
	} else {
		lista.ultimo.siguiente = nuevo_nodo
		lista.ultimo = nuevo_nodo
	}
	lista.largo++
}

func (lista *listaEnlazada[T]) BorrarPrimero() T {
	if lista.EstaVacia() {
		panic(lista_vacia)
	}
	dato := lista.primero.dato
	lista.primero = lista.primero.siguiente
	lista.largo--
	return dato
}

func (lista *listaEnlazada[T]) Iterar(visitar func(T) bool) {
	actual := lista.primero
	for actual != nil && visitar(actual.dato) {
		actual = actual.siguiente
	}
}

type iteradorLista[T any] struct {
	actual   *nodoLista[T]
	anterior *nodoLista[T]
	lista    *listaEnlazada[T]
}

func (lista *listaEnlazada[T]) Iterador() IteradorLista[T] {
	iterador := new(iteradorLista[T])
	iterador.lista = lista
	iterador.actual = iterador.lista.primero
	return iterador
}

func (iterador iteradorLista[T]) VerActual() T {
	if !iterador.HaySiguiente() {
		panic(iterador_vacio)
	}
	return iterador.actual.dato
}

func (iterador iteradorLista[T]) HaySiguiente() bool {
	return iterador.actual != nil
}

func (iterador *iteradorLista[T]) Siguiente() {
	if !iterador.HaySiguiente() {
		panic(iterador_vacio)
	}
	iterador.anterior = iterador.actual
	iterador.actual = iterador.actual.siguiente
}

func (iterador *iteradorLista[T]) Insertar(dato T) {
	nuevo_nodo := crearNodo[T](dato)
	if iterador.anterior == nil && iterador.actual == nil {
		iterador.lista.primero = nuevo_nodo
		iterador.lista.ultimo = nuevo_nodo
		iterador.actual = iterador.lista.primero
	} else if iterador.anterior == nil {
		nuevo_nodo.siguiente = iterador.actual
		iterador.actual = nuevo_nodo
		iterador.lista.primero = iterador.actual
	} else {
		iterador.anterior.siguiente = nuevo_nodo
		nuevo_nodo.siguiente = iterador.actual
		iterador.actual = nuevo_nodo
		if iterador.actual.siguiente == nil {
			iterador.lista.ultimo = iterador.actual
		}
	}
	iterador.lista.largo++

}

func (iterador *iteradorLista[T]) Borrar() T {
	if !iterador.HaySiguiente() {
		panic(iterador_vacio)
	}
	dato := iterador.actual.dato
	iterador.lista.largo--
	if iterador.anterior == nil {
		if iterador.actual.siguiente != nil {
			iterador.actual = iterador.actual.siguiente
			iterador.lista.primero = iterador.actual
			return dato
		} else {
			iterador.actual = nil
			return dato
		}
	}
	iterador.anterior.siguiente = iterador.actual.siguiente
	if iterador.actual.siguiente == nil {
		iterador.actual = nil
		iterador.lista.ultimo = iterador.anterior
		return dato
	}
	iterador.actual = iterador.actual.siguiente
	return dato
}
