package lista_test

import (
	TDALista "tdas/lista"
	"testing"

	"github.com/stretchr/testify/require"
)

const lista_vacia = "La lista esta vacia"
const iterador_vacio = "El iterador termino de iterar"

func TestListaVacia(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	require.True(t, lista.EstaVacia())
	require.PanicsWithValue(t, lista_vacia, func() { lista.BorrarPrimero() })
	require.PanicsWithValue(t, lista_vacia, func() { lista.VerPrimero() })
	require.PanicsWithValue(t, lista_vacia, func() { lista.VerUltimo() })
	require.EqualValues(t, 0, lista.Largo())
}

func TestOrdenLista(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(2)
	require.False(t, lista.EstaVacia())
	require.EqualValues(t, 2, lista.VerPrimero())
	require.EqualValues(t, 2, lista.VerUltimo())
	require.EqualValues(t, 1, lista.Largo())
	lista.InsertarPrimero(1)
	require.EqualValues(t, 1, lista.VerPrimero())
	require.EqualValues(t, 2, lista.VerUltimo())
	require.EqualValues(t, 2, lista.Largo())
	lista.InsertarUltimo(3)
	require.EqualValues(t, 1, lista.VerPrimero())
	require.EqualValues(t, 3, lista.VerUltimo())
	require.EqualValues(t, 3, lista.Largo())
	require.EqualValues(t, 1, lista.BorrarPrimero())
	require.EqualValues(t, 2, lista.VerPrimero())
	require.EqualValues(t, 3, lista.VerUltimo())
	require.EqualValues(t, 2, lista.Largo())
	require.EqualValues(t, 2, lista.BorrarPrimero())
	require.EqualValues(t, 3, lista.VerPrimero())
	require.EqualValues(t, 3, lista.VerUltimo())
	require.EqualValues(t, 1, lista.Largo())
	require.EqualValues(t, 3, lista.BorrarPrimero())
	require.PanicsWithValue(t, lista_vacia, func() { lista.VerPrimero() })
	require.PanicsWithValue(t, lista_vacia, func() { lista.VerUltimo() })
	require.EqualValues(t, 0, lista.Largo())
	require.True(t, lista.EstaVacia())
}

func TestVolumenLista(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	for i := 1; i < 10000; i++ {
		lista.InsertarPrimero(i) //Primero con InsertarPrimero
		require.False(t, lista.EstaVacia())
		require.EqualValues(t, i, lista.Largo())
	}
	for i := 1; i < 10000; i++ {
		require.EqualValues(t, 10000-i, lista.VerPrimero())
		require.EqualValues(t, 1, lista.VerUltimo())
		require.False(t, lista.EstaVacia())
		require.EqualValues(t, 10000-i, lista.Largo())
		require.EqualValues(t, 10000-i, lista.BorrarPrimero())
	}
	require.True(t, lista.EstaVacia())
	for i := 1; i < 10000; i++ {
		lista.InsertarUltimo(i) //Ahora con InsertarUltimo
		require.EqualValues(t, i, lista.Largo())
		require.False(t, lista.EstaVacia())
	}
	for i := 1; i < 10000; i++ {
		require.EqualValues(t, 9999, lista.VerUltimo())
		require.EqualValues(t, i, lista.VerPrimero())
		require.False(t, lista.EstaVacia())
		require.EqualValues(t, 10000-i, lista.Largo())
		require.EqualValues(t, i, lista.BorrarPrimero())
	}
	require.True(t, lista.EstaVacia())

}

func TestListaVaciada(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	require.True(t, lista.EstaVacia())
	lista.InsertarPrimero(1)
	lista.InsertarUltimo(2)
	lista.InsertarUltimo(3)
	require.False(t, lista.EstaVacia())
	require.EqualValues(t, 3, lista.Largo())
	lista.BorrarPrimero()
	lista.BorrarPrimero()
	lista.BorrarPrimero()
	require.EqualValues(t, 0, lista.Largo())
	require.PanicsWithValue(t, lista_vacia, func() { lista.BorrarPrimero() })
	require.PanicsWithValue(t, lista_vacia, func() { lista.VerPrimero() })
	require.PanicsWithValue(t, lista_vacia, func() { lista.VerUltimo() })
}

func TestErroresListaVacia(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[bool]()
	require.PanicsWithValue(t, lista_vacia, func() { lista.BorrarPrimero() })
	require.PanicsWithValue(t, lista_vacia, func() { lista.VerPrimero() })
	require.PanicsWithValue(t, lista_vacia, func() { lista.VerUltimo() })
}

func TestListaVaciaEsVerdadero(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[bool]()
	require.True(t, lista.EstaVacia())
}

func TestListaDistintosTipos(t *testing.T) {
	lista_bool := TDALista.CrearListaEnlazada[bool]()
	lista_bool.InsertarPrimero(true)
	lista_bool.InsertarPrimero(true)
	lista_bool.InsertarUltimo(false)
	require.EqualValues(t, true, lista_bool.VerPrimero())
	require.EqualValues(t, false, lista_bool.VerUltimo())
	require.EqualValues(t, true, lista_bool.BorrarPrimero())
	require.EqualValues(t, true, lista_bool.VerPrimero())
	require.EqualValues(t, false, lista_bool.VerUltimo())
	require.EqualValues(t, true, lista_bool.BorrarPrimero())
	require.EqualValues(t, false, lista_bool.VerPrimero())
	require.EqualValues(t, false, lista_bool.VerUltimo())
	require.EqualValues(t, false, lista_bool.BorrarPrimero())
	require.True(t, lista_bool.EstaVacia())
	lista_any := TDALista.CrearListaEnlazada[any]()
	lista_any.InsertarPrimero(2)
	lista_any.InsertarPrimero("1")
	lista_any.InsertarUltimo(true)
	require.EqualValues(t, "1", lista_any.VerPrimero())
	require.EqualValues(t, true, lista_any.VerUltimo())
	require.EqualValues(t, "1", lista_any.BorrarPrimero())
	require.EqualValues(t, 2, lista_any.VerPrimero())
	require.EqualValues(t, true, lista_any.VerUltimo())
	require.EqualValues(t, 2, lista_any.BorrarPrimero())
	require.EqualValues(t, true, lista_any.VerPrimero())
	require.EqualValues(t, true, lista_any.VerUltimo())
	require.EqualValues(t, true, lista_any.BorrarPrimero())
	require.True(t, lista_any.EstaVacia())

}

func TestIterar(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(3)
	lista.InsertarPrimero(2)
	lista.InsertarPrimero(1)
	cont := 0
	lista.Iterar(func(v int) bool {
		if v%2 == 0 {
			cont++
		}
		return true
	})
	require.EqualValues(t, 1, cont)
	lista.InsertarUltimo(4)
	cont = 0
	lista.Iterar(func(v int) bool {
		if v%2 == 0 {
			cont++
		}
		return v != 3
	})
	require.EqualValues(t, 1, cont)
}

func TestIterarListaVacia(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.Iterar(func(v int) bool {
		return v != 1
	})
}

func TestIteradorInsertarAlPrincipio(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(3)
	lista.InsertarPrimero(2)
	lista.InsertarPrimero(1)
	iter := lista.Iterador()
	iter.Insertar(0)
	require.EqualValues(t, 0, lista.VerPrimero())
	require.EqualValues(t, 4, lista.Largo())
}

func TestIteradorInsertarAlFinal(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(3)
	lista.InsertarPrimero(2)
	lista.InsertarPrimero(1)
	iter := lista.Iterador()
	for iter.HaySiguiente() {
		iter.Siguiente()
	}
	iter.Insertar(4)
	require.EqualValues(t, 4, lista.VerUltimo())
	require.EqualValues(t, 4, lista.Largo())
}

func TestIteradorInsertarEnElMedio(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(4)
	lista.InsertarPrimero(2)
	lista.InsertarPrimero(1)
	iter := lista.Iterador()
	iter.Siguiente()
	iter.Siguiente()
	iter.Insertar(3)
	iter_aux := lista.Iterador()
	for i := 1; i < 5; i++ {
		require.EqualValues(t, i, iter_aux.VerActual())
		iter_aux.Siguiente()
	}
}

func TestRemoverPrimerElemento(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(3)
	lista.InsertarPrimero(2)
	lista.InsertarPrimero(1)
	iter := lista.Iterador()
	iter.Borrar()
	require.EqualValues(t, 2, lista.Largo())
	require.EqualValues(t, 2, lista.VerPrimero())
	require.EqualValues(t, 3, lista.VerUltimo())
}

func TestRemoverUltimoElemento(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(3)
	lista.InsertarPrimero(2)
	lista.InsertarPrimero(1)
	iter := lista.Iterador()
	for iter.HaySiguiente() {
		if iter.VerActual() == 3 {
			iter.Borrar()
		} else {
			iter.Siguiente()
		}
	}
	require.EqualValues(t, 2, lista.Largo())
	require.EqualValues(t, 1, lista.VerPrimero())
	require.EqualValues(t, 2, lista.VerUltimo())
}

func TestRemoverElementoDelMedio(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(3)
	lista.InsertarPrimero(2)
	lista.InsertarPrimero(1)
	iter := lista.Iterador()
	for iter.HaySiguiente() {
		if iter.VerActual() == 2 {
			iter.Borrar()
		} else {
			iter.Siguiente()
		}
	}
	require.EqualValues(t, 2, lista.Largo())
	require.EqualValues(t, 1, lista.VerPrimero())
	require.EqualValues(t, 3, lista.VerUltimo())
}

func TestIteradorSobreListaVacia(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[string]()
	iter := lista.Iterador()
	require.False(t, iter.HaySiguiente())
	require.PanicsWithValue(t, iterador_vacio, func() { iter.Borrar() })
	require.PanicsWithValue(t, iterador_vacio, func() { iter.Siguiente() })
	require.PanicsWithValue(t, iterador_vacio, func() { iter.VerActual() })
}

func TestIteradorSobreListaVaciada(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(3)
	lista.InsertarPrimero(2)
	lista.InsertarPrimero(1)
	iter := lista.Iterador()
	for iter.HaySiguiente() {
		iter.Borrar()
	}
	require.EqualValues(t, 0, lista.Largo())
	require.False(t, iter.HaySiguiente())
	require.PanicsWithValue(t, iterador_vacio, func() { iter.Borrar() })
	require.PanicsWithValue(t, iterador_vacio, func() { iter.Siguiente() })
	require.PanicsWithValue(t, iterador_vacio, func() { iter.VerActual() })
}

func TestErroresEnListaIterada(t *testing.T) {
	lista := TDALista.CrearListaEnlazada[int]()
	lista.InsertarPrimero(3)
	lista.InsertarPrimero(2)
	lista.InsertarPrimero(1)
	iter := lista.Iterador()
	for iter.HaySiguiente() {
		iter.Siguiente()
	}
	require.EqualValues(t, 3, lista.Largo())
	require.False(t, iter.HaySiguiente())
	require.PanicsWithValue(t, iterador_vacio, func() { iter.Borrar() })
	require.PanicsWithValue(t, iterador_vacio, func() { iter.Siguiente() })
	require.PanicsWithValue(t, iterador_vacio, func() { iter.VerActual() })
}

func TestVolumenIterador(t *testing.T) {
	lista_borrar := TDALista.CrearListaEnlazada[int]()
	for i := 1; i < 10000; i++ {
		lista_borrar.InsertarUltimo(i)
	}
	iter_borrar := lista_borrar.Iterador()
	for i := 1; i < 10000; i++ {
		require.True(t, iter_borrar.HaySiguiente())
		require.EqualValues(t, i, iter_borrar.VerActual())
		require.EqualValues(t, i, iter_borrar.Borrar())
	}
	require.EqualValues(t, 0, lista_borrar.Largo())
	lista_insertar := TDALista.CrearListaEnlazada[int]()
	for i := 1; i < 10000; i += 2 {
		lista_insertar.InsertarUltimo(i)
	}
	iter_insertar := lista_insertar.Iterador()
	for i := 0; i < 10000; i += 2 {
		iter_insertar.Insertar(i)
		iter_insertar.Siguiente()
		iter_insertar.Siguiente()

	}
	for i := 0; i < 10000; i++ {
		require.EqualValues(t, i, lista_insertar.VerPrimero())
		require.EqualValues(t, 10000-i, lista_insertar.Largo())
		require.EqualValues(t, i, lista_insertar.VerPrimero())
		require.EqualValues(t, i, lista_insertar.BorrarPrimero())
	}
}
