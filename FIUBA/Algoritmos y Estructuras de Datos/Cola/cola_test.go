package cola_test

import (
	TDACola "tdas/cola"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestColaVacia(t *testing.T) {
	cola := TDACola.CrearColaEnlazada[int]()
	require.True(t, cola.EstaVacia())
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola.VerPrimero() })
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola.Desencolar() })
}

func TestFIFO(t *testing.T) {
	cola_int := TDACola.CrearColaEnlazada[int]()
	cola_int.Encolar(1)
	cola_int.Encolar(2)
	cola_int.Encolar(3)
	require.EqualValues(t, 1, cola_int.Desencolar())
	require.EqualValues(t, 2, cola_int.Desencolar())
	require.False(t, cola_int.EstaVacia())
	require.EqualValues(t, 3, cola_int.Desencolar())
	require.True(t, cola_int.EstaVacia())
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_int.VerPrimero() })
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_int.Desencolar() })
	cola_str := TDACola.CrearColaEnlazada[string]()
	cola_str.Encolar("1")
	cola_str.Encolar("2")
	cola_str.Encolar("3")
	require.EqualValues(t, "1", cola_str.Desencolar())
	require.False(t, cola_str.EstaVacia())
	require.EqualValues(t, "2", cola_str.Desencolar())
	require.EqualValues(t, "3", cola_str.Desencolar())
	require.True(t, cola_str.EstaVacia())
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_str.VerPrimero() })
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_str.Desencolar() })
}

func TestVolumen(t *testing.T) {
	cola := TDACola.CrearColaEnlazada[int]()
	for i := 1; i < 10000; i++ {
		cola.Encolar(i)
		require.False(t, cola.EstaVacia())
	}
	for i := 1; i < 10000; i++ {
		require.EqualValues(t, i, cola.Desencolar())
		if !cola.EstaVacia() {
			require.EqualValues(t, i+1, cola.VerPrimero())
		}
	}
	require.True(t, cola.EstaVacia())
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola.VerPrimero() })
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola.Desencolar() })
}

func TestColaDesencolada(t *testing.T) {
	cola_int := TDACola.CrearColaEnlazada[int]()
	cola_int.Encolar(1)
	cola_int.Encolar(2)
	cola_int.Encolar(3)
	require.EqualValues(t, 1, cola_int.VerPrimero())
	cola_int.Desencolar()
	require.EqualValues(t, 2, cola_int.VerPrimero())
	cola_int.Desencolar()
	require.EqualValues(t, 3, cola_int.VerPrimero())
	cola_int.Desencolar()
	require.True(t, cola_int.EstaVacia())
}

func TestErroresColaVacia(t *testing.T) {
	cola := TDACola.CrearColaEnlazada[int]()
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola.VerPrimero() })
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola.Desencolar() })
}

func TestColaVaciaEsVerdadero(t *testing.T) {
	cola := TDACola.CrearColaEnlazada[int]()
	require.True(t, cola.EstaVacia())
}

func TestColaDesencoladaErrores(t *testing.T) {
	cola_int := TDACola.CrearColaEnlazada[int]()
	cola_int.Encolar(1)
	cola_int.Encolar(2)
	cola_int.Encolar(3)
	cola_int.Desencolar()
	cola_int.Desencolar()
	cola_int.Desencolar()
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_int.VerPrimero() })
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_int.Desencolar() })
}

func TestEncolarDistintosTipos(t *testing.T) {
	cola_bool := TDACola.CrearColaEnlazada[bool]()
	cola_bool.Encolar(true)
	cola_bool.Encolar(false)
	cola_bool.Encolar(false)
	require.True(t, cola_bool.Desencolar())
	require.False(t, cola_bool.Desencolar())
	require.False(t, cola_bool.EstaVacia())
	require.False(t, cola_bool.Desencolar())
	require.True(t, cola_bool.EstaVacia())
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_bool.VerPrimero() })
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_bool.Desencolar() })
	cola_any := TDACola.CrearColaEnlazada[any]()
	cola_any.Encolar(1)
	cola_any.Encolar("2")
	cola_any.Encolar(true)
	require.EqualValues(t, 1, cola_any.Desencolar())
	require.EqualValues(t, "2", cola_any.Desencolar())
	require.False(t, cola_any.EstaVacia())
	require.EqualValues(t, true, cola_any.Desencolar())
	require.True(t, cola_any.EstaVacia())
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_any.VerPrimero() })
	require.PanicsWithValue(t, "La cola esta vacia", func() { cola_any.Desencolar() })
}
