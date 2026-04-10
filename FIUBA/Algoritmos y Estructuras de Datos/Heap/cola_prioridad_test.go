package cola_prioridad_test

import (
	TDAHeap "tdas/cola_prioridad"
	"testing"

	"github.com/stretchr/testify/require"
)

func cmp(a, b int) int {
	return a - b
}

func cmpFloat(a, b float64) int {
	diff := a - b
	if diff > 0 {
		return 1
	} else if diff < 0 {
		return -1
	}
	return 0
}

func cmpBool(a, b bool) int {
	if a && !b {
		return 1
	} else if !a && b {
		return -1
	}
	return 0
}

func cmpString(a, b string) int {
	return len(a) - len(b)
}

func TestHeapVacio(t *testing.T) {
	heap := TDAHeap.CrearHeap(cmp)
	require.True(t, heap.EstaVacia())
	require.EqualValues(t, 0, heap.Cantidad())
	require.Panics(t, func() { heap.VerMax() })
	require.Panics(t, func() { heap.Desencolar() })
	require.True(t, heap.EstaVacia())
}

func TestHeapVolumen(t *testing.T) {
	heap := TDAHeap.CrearHeap(cmp)
	volumen := 10000

	for i := 0; i < volumen; i++ {
		heap.Encolar(i)
		require.False(t, heap.EstaVacia())
		require.Equal(t, i, heap.VerMax())
	}
	require.False(t, heap.EstaVacia())
	require.Equal(t, volumen, heap.Cantidad())

	for i := volumen - 1; i >= 0; i-- {
		require.False(t, heap.EstaVacia())
		require.Equal(t, i, heap.VerMax())
		require.Equal(t, i, heap.Desencolar())
	}
	require.True(t, heap.EstaVacia())
	require.Equal(t, 0, heap.Cantidad())
}

func TestHeapTiposDiferentes(t *testing.T) {
	heapInt := TDAHeap.CrearHeap[int](cmp)
	heapStr := TDAHeap.CrearHeap[string](cmpString)
	heapBool := TDAHeap.CrearHeap[bool](cmpBool)
	heapFloat := TDAHeap.CrearHeap[float64](cmpFloat)

	heapInt.Encolar(1)
	heapInt.Encolar(2)
	heapInt.Encolar(3)
	require.Equal(t, 3, heapInt.VerMax())
	require.Equal(t, 3, heapInt.Desencolar())
	require.Equal(t, 2, heapInt.VerMax())
	require.Equal(t, 2, heapInt.Cantidad())

	heapStr.Encolar("Algo")
	heapStr.Encolar("Programacion")
	require.False(t, heapStr.EstaVacia())
	require.Equal(t, "Programacion", heapStr.VerMax())
	require.Equal(t, "Programacion", heapStr.Desencolar())
	require.Equal(t, "Algo", heapStr.VerMax())
	require.Equal(t, 1, heapStr.Cantidad())

	heapBool.Encolar(true)
	heapBool.Encolar(false)
	require.False(t, heapBool.EstaVacia())
	require.Equal(t, true, heapBool.VerMax())
	require.Equal(t, true, heapBool.Desencolar())
	require.Equal(t, false, heapBool.VerMax())

	heapFloat.Encolar(13.45)
	heapFloat.Encolar(100.89)
	require.False(t, heapFloat.EstaVacia())
	require.Equal(t, 100.89, heapFloat.VerMax())
	require.Equal(t, 100.89, heapFloat.Desencolar())
	require.Equal(t, 13.45, heapFloat.VerMax())
}

func TestHeapConPocosElementos(t *testing.T) {
	heap := TDAHeap.CrearHeap[int](cmp)
	elementos := []int{1, 2, 3}

	heap.Encolar(elementos[0])
	heap.Encolar(elementos[1])
	require.False(t, heap.EstaVacia())
	require.Equal(t, elementos[1], heap.VerMax())
	require.Equal(t, elementos[1], heap.Desencolar())

	require.Equal(t, elementos[0], heap.VerMax())

	heap.Encolar(elementos[2])
	require.Equal(t, elementos[2], heap.VerMax())
	require.False(t, heap.EstaVacia())

	require.Equal(t, elementos[2], heap.Desencolar())

	require.Equal(t, elementos[0], heap.Desencolar())

	require.True(t, heap.EstaVacia())
}

func TestHeapDesencolarHastaVacia(t *testing.T) {
	heap := TDAHeap.CrearHeap[int](cmp)
	elementos := []int{1, 2, 3, 4, 5}

	for _, elemento := range elementos {
		heap.Encolar(elemento)
	}

	for i := len(elementos) - 1; i >= 0; i-- {
		require.Equal(t, elementos[i], heap.Desencolar())
	}

	require.True(t, heap.EstaVacia())
	require.Panics(t, func() { heap.VerMax() })
	require.Panics(t, func() { heap.Desencolar() })
}

func TestHeapInvalido(t *testing.T) {
	heap := TDAHeap.CrearHeap[int](cmp)
	heap.Encolar(1)
	require.Equal(t, 1, heap.Desencolar())
	require.Panics(t, func() { heap.VerMax() })
	require.Panics(t, func() { heap.Desencolar() })
}

func TestHeapsort(t *testing.T) {
	heap := []int{23, 40, 14, 57, 10, 3, 7, 1000}
	heapOrdenado := []int{3, 7, 10, 14, 23, 40, 57, 1000}
	TDAHeap.HeapSort(heap, cmp)
	require.Equal(t, heapOrdenado, heap)
}

func TestCrearHeapArr(t *testing.T) {
	arreglo := []int{1, 8, 12, 4, 2, 20}
	heap := TDAHeap.CrearHeapArr(arreglo, cmp)

	require.False(t, heap.EstaVacia())
	require.Equal(t, 20, heap.VerMax())
	require.Equal(t, 6, heap.Cantidad())

	heap.Desencolar()
	require.False(t, heap.EstaVacia())
	require.Equal(t, 12, heap.VerMax())
	require.Equal(t, 5, heap.Cantidad())

	heap.Desencolar()
	require.False(t, heap.EstaVacia())
	require.Equal(t, 8, heap.VerMax())
	require.Equal(t, 4, heap.Cantidad())

	heap.Desencolar()
	require.False(t, heap.EstaVacia())
	require.Equal(t, 4, heap.VerMax())
	require.Equal(t, 3, heap.Cantidad())

	heap.Desencolar()
	require.False(t, heap.EstaVacia())
	require.Equal(t, 2, heap.VerMax())
	require.Equal(t, 2, heap.Cantidad())

	heap.Desencolar()
	require.False(t, heap.EstaVacia())
	require.Equal(t, 1, heap.VerMax())
	require.Equal(t, 1, heap.Cantidad())

	heap.Desencolar()
	require.True(t, heap.EstaVacia())
	require.Panics(t, func() { heap.VerMax() })
	require.Panics(t, func() { heap.Desencolar() })
	require.Equal(t, 0, heap.Cantidad())

}
