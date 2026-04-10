package cola_prioridad

const (
	TAMAÑO_INICIAL       = 5
	REDIMENSION_ACHICAR  = 2
	REDIMENSION_AGRANDAR = 2
)

type heap[T any] struct {
	datos    []T
	cantidad int
	cmp      fcmpHeap[T]
}

type fcmpHeap[T any] func(T, T) int

func CrearHeap[T any](funcion_cmp fcmpHeap[T]) ColaPrioridad[T] {
	heap := new(heap[T])
	heap.cmp = funcion_cmp
	heap.datos = make([]T, TAMAÑO_INICIAL)
	return heap
}

func (h heap[T]) EstaVacia() bool {
	return h.cantidad == 0
}

func (h heap[T]) VerMax() T {
	if h.EstaVacia() {
		panic("La cola esta vacia")
	}
	return h.datos[0]
}

func (h heap[T]) Cantidad() int {
	return h.cantidad
}

func buscarHijos(pos_padre int) (int, int) {
	pos_hijo_izq := 2*pos_padre + 1
	pos_hijo_der := 2*pos_padre + 2
	return pos_hijo_izq, pos_hijo_der
}

func buscarPadre(pos_hijo int) int {
	pos_padre := (pos_hijo - 1) / 2
	return pos_padre
}

func (h *heap[T]) redimensionar(nuevo_tam int) {
	nuevo := make([]T, nuevo_tam)
	copy(nuevo, h.datos)
	h.datos = nuevo
}

func upHeap[T any](arreglo []T, pos_hijo int, funcion_cmp fcmpHeap[T]) {
	if pos_hijo == 0 {
		return
	}
	pos_padre := buscarPadre(pos_hijo)
	if funcion_cmp(arreglo[pos_hijo], arreglo[pos_padre]) > 0 {
		arreglo[pos_padre], arreglo[pos_hijo] = arreglo[pos_hijo], arreglo[pos_padre]
		upHeap(arreglo, pos_padre, funcion_cmp)
	}
}

func downHeap[T any](arreglo []T, tam, pos_padre int, funcion_cmp fcmpHeap[T]) {
	pos_hijo_izq, pos_hijo_der := buscarHijos(pos_padre)
	max := pos_padre
	if pos_hijo_izq < tam && funcion_cmp(arreglo[pos_hijo_izq], arreglo[max]) > 0 {
		max = pos_hijo_izq
	}
	if pos_hijo_der < tam && funcion_cmp(arreglo[pos_hijo_der], arreglo[max]) > 0 {
		max = pos_hijo_der
	}
	if max != pos_padre {
		arreglo[pos_padre], arreglo[max] = arreglo[max], arreglo[pos_padre]
		downHeap(arreglo, tam, max, funcion_cmp)
	}
}

func heapify[T any](arreglo []T, funcion_cmp fcmpHeap[T]) {
	for i := len(arreglo); i >= 0; i-- {
		downHeap(arreglo, len(arreglo), i, funcion_cmp)
	}
}

func CrearHeapArr[T any](arreglo []T, funcion_cmp fcmpHeap[T]) ColaPrioridad[T] {
	heap := new(heap[T])
	heap.cmp = funcion_cmp
	longitud := len(arreglo)
	if longitud == 0 {
		longitud = 2
	}
	heap.datos = make([]T, longitud)
	copy(heap.datos, arreglo)
	heap.cantidad = len(arreglo)
	heapify(heap.datos, heap.cmp)
	return heap
}

func HeapSort[T any](arreglo []T, funcion_cmp fcmpHeap[T]) {
	heapify(arreglo, funcion_cmp)
	for i := len(arreglo) - 1; i > 0; i-- {
		arreglo[0], arreglo[i] = arreglo[i], arreglo[0]
		downHeap(arreglo, i, 0, funcion_cmp)
	}
}

func (h *heap[T]) Encolar(dato T) {
	if h.cantidad == cap(h.datos) {
		h.redimensionar(cap(h.datos) * REDIMENSION_AGRANDAR)
	}
	h.datos[h.cantidad] = dato
	upHeap(h.datos, h.cantidad, h.cmp)
	h.cantidad++
}

func (h *heap[T]) Desencolar() T {
	if h.EstaVacia() {
		panic("La cola esta vacia")
	}
	if h.cantidad*4 <= cap(h.datos) && cap(h.datos) > TAMAÑO_INICIAL {
		h.redimensionar(cap(h.datos) / REDIMENSION_ACHICAR)
	}
	maximo := h.datos[0]
	h.datos[0] = h.datos[h.cantidad-1]
	h.cantidad--
	downHeap(h.datos, h.cantidad, 0, h.cmp)
	return maximo
}
