package pila_test

import (
	TDAPila "tdas/pila"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestPilaVacia(t *testing.T) {
	//No termino de entender lo que debería verificar esta prueba.
	//Entiendo que es lo mismo que TestErroresPilaVacia y TestPilaVaciaIsTrue,
	//pero como se pide una prueba por cada situacion de la pagina de la materia,
	//por las dudas tambien incluyo esta prueba

	pila := TDAPila.CrearPilaDinamica[int]()
	require.True(t, pila.EstaVacia())
	require.PanicsWithValue(t, "La pila esta vacia", func() { pila.VerTope() })
	require.PanicsWithValue(t, "La pila esta vacia", func() { pila.Desapilar() })
}

func TestLIFO(t *testing.T) {
	pila_int := TDAPila.CrearPilaDinamica[int]()
	pila_int.Apilar(1)
	pila_int.Apilar(2)
	pila_int.Apilar(3)
	require.EqualValues(t, 3, pila_int.Desapilar())
	require.EqualValues(t, 2, pila_int.Desapilar())
	require.EqualValues(t, 1, pila_int.Desapilar())
	pila_str := TDAPila.CrearPilaDinamica[string]()
	pila_str.Apilar("1")
	pila_str.Apilar("2")
	pila_str.Apilar("3")
	require.EqualValues(t, "3", pila_str.Desapilar())
	require.EqualValues(t, "2", pila_str.Desapilar())
	require.EqualValues(t, "1", pila_str.Desapilar())
}

func TestVolumen(t *testing.T) {
	pila := TDAPila.CrearPilaDinamica[int]()
	for i := 1; i < 10000; i++ {
		pila.Apilar(i)
	}
	for i := 1; i < 10000; i++ {
		require.EqualValues(t, 10000-i, pila.Desapilar())
		if pila.EstaVacia() == false {
			require.EqualValues(t, 10000-i-1, pila.VerTope())
		}
	}
}

func TestPilaDesapilada(t *testing.T) {
	pila_int := TDAPila.CrearPilaDinamica[int]()
	pila_int.Apilar(1)
	pila_int.Apilar(2)
	pila_int.Apilar(3)
	require.EqualValues(t, 3, pila_int.VerTope())
	pila_int.Desapilar()
	require.EqualValues(t, 2, pila_int.VerTope())
	pila_int.Desapilar()
	require.EqualValues(t, 1, pila_int.VerTope())
	pila_int.Desapilar()
	require.True(t, pila_int.EstaVacia())
}

func TestErroresPilaVacia(t *testing.T) {
	pila := TDAPila.CrearPilaDinamica[int]()
	require.PanicsWithValue(t, "La pila esta vacia", func() { pila.VerTope() })
	require.PanicsWithValue(t, "La pila esta vacia", func() { pila.Desapilar() })
}

func TestPilaVaciaIsTrue(t *testing.T) {
	pila := TDAPila.CrearPilaDinamica[int]()
	require.True(t, pila.EstaVacia())
}

func TestPilaDesapiladaErrores(t *testing.T) {
	pila_int := TDAPila.CrearPilaDinamica[int]()
	pila_int.Apilar(1)
	pila_int.Apilar(2)
	pila_int.Apilar(3)
	pila_int.Desapilar()
	pila_int.Desapilar()
	pila_int.Desapilar()
	require.PanicsWithValue(t, "La pila esta vacia", func() { pila_int.VerTope() })
	require.PanicsWithValue(t, "La pila esta vacia", func() { pila_int.Desapilar() })
}

func TestApilarDistintosTipos(t *testing.T) {
	pila_bool := TDAPila.CrearPilaDinamica[bool]()
	pila_bool.Apilar(true)
	pila_bool.Apilar(false)
	pila_bool.Apilar(false)
	require.False(t, pila_bool.Desapilar())
	require.False(t, pila_bool.Desapilar())
	require.True(t, pila_bool.Desapilar())
	require.True(t, pila_bool.EstaVacia())
	pila_any := TDAPila.CrearPilaDinamica[any]()
	pila_any.Apilar(1)
	pila_any.Apilar("2")
	pila_any.Apilar(true)
	require.EqualValues(t, true, pila_any.Desapilar())
	require.EqualValues(t, "2", pila_any.Desapilar())
	require.EqualValues(t, 1, pila_any.Desapilar())
	require.True(t, pila_any.EstaVacia())
}
