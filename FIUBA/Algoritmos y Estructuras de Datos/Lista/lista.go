package lista

type Lista[T any] interface {

	// EstaVacia devuelve verdadero si la lista no tiene elementos, false en caso contrario.
	EstaVacia() bool

	// InsertarPrimero coloca un elemento al principio de la lista.
	InsertarPrimero(T)

	// InsertarUltimo coloca un elemento al final de lista.
	InsertarUltimo(T)

	// BorrarPrimero borra el primer elemento de la lista y lo devuelve.
	// Si está vacía, entra en pánico con un mensaje "La lista esta vacia".
	BorrarPrimero() T

	// VerPrimero devuelve el primer elemento de la lista.
	// Si está vacía, entra en pánico con un mensaje "La lista esta vacia".
	VerPrimero() T

	// VerUltimo devuelve el último elemento de la lista.
	// Si está vacía, entra en pánico con un mensaje "La lista esta vacia".
	VerUltimo() T

	// Largo devuelve la cantidad de elementos de la lista.
	Largo() int

	// Iterar aplica la función pasada por parámetro a todos los elementos de la lista, hasta que no hayan más
	// elementos, o la función en cuestión devuelva false.
	Iterar(visitar func(T) bool)

	// Devuelve una instancia de IteradorLista.
	Iterador() IteradorLista[T]
}

type IteradorLista[T any] interface {

	// Devuelve el elemento actual de la iteración.Si se la invoca sobre un iterador que ya haya iterado
	// todos los elementos, entra en panico con el mensaje "El iterador termino de iterar"
	VerActual() T

	// Devuelve si hay algún elemento para ver en la posicion actual
	HaySiguiente() bool

	// Avanza una posicion en la iteración.Si se la invoca sobre un iterador que ya haya iterado
	// todos los elementos, entra en panico con el mensaje "El iterador termino de iterar"
	Siguiente()

	// Inserta un elemento en la posición actual
	Insertar(T)

	// Borra el elemento de la posicion actual. Si se la invoca sobre un iterador que ya haya iterado
	// todos los elementos, entra en panico con el mensaje "El iterador termino de iterar"
	Borrar() T
}
