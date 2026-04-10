package diccionario_test

import (
	"fmt"
	"math/rand"
	TDADiccionario "tdas/diccionario"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
)

func compNums(a, b int) int {
	return a - b
}

func compStr(a, b string) int {
	if a > b {
		return 1
	} else if b > a {
		return -1
	}
	return 0
}

var TAM_VOLUMEN = []int{1250, 2500, 5000, 10000, 20000, 40000}

func TestDiccVacio(t *testing.T) {
	t.Log("Comprueba que Arbol vacio no tiene claves")
	dic := TDADiccionario.CrearABB[string, string](compStr)
	require.EqualValues(t, 0, dic.Cantidad())
	require.False(t, dic.Pertenece("A"))
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Obtener("A") })
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Borrar("A") })
}

func TestDiccClaveDefault(t *testing.T) {
	t.Log("Prueba sobre un Arbol vacío que si justo buscamos la clave que es el default del tipo de dato, " +
		"sigue sin existir")
	dic := TDADiccionario.CrearABB[string, string](compStr)
	require.False(t, dic.Pertenece(""))
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Obtener("") })
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Borrar("") })

	dicNum := TDADiccionario.CrearABB[int, string](compNums)
	require.False(t, dicNum.Pertenece(0))
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dicNum.Obtener(0) })
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dicNum.Borrar(0) })
}

func TestUnElemento(t *testing.T) {
	t.Log("Comprueba que ABB con un elemento tiene esa Clave, unicamente")
	dic := TDADiccionario.CrearABB[string, int](compStr)
	dic.Guardar("A", 10)
	require.EqualValues(t, 1, dic.Cantidad())
	require.True(t, dic.Pertenece("A"))
	require.False(t, dic.Pertenece("B"))
	require.EqualValues(t, 10, dic.Obtener("A"))
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Obtener("B") })
}

func TestDiccGuardar(t *testing.T) {
	t.Log("Guarda algunos pocos elementos en el ABB, y se comprueba que en todo momento funciona acorde")
	clave1 := "Gato"
	clave2 := "Perro"
	clave3 := "Vaca"
	valor1 := "miau"
	valor2 := "guau"
	valor3 := "moo"
	claves := []string{clave1, clave2, clave3}
	valores := []string{valor1, valor2, valor3}

	dic := TDADiccionario.CrearABB[string, string](compStr)
	require.False(t, dic.Pertenece(claves[0]))
	require.False(t, dic.Pertenece(claves[0]))
	dic.Guardar(claves[0], valores[0])
	require.EqualValues(t, 1, dic.Cantidad())
	require.True(t, dic.Pertenece(claves[0]))
	require.True(t, dic.Pertenece(claves[0]))
	require.EqualValues(t, valores[0], dic.Obtener(claves[0]))
	require.EqualValues(t, valores[0], dic.Obtener(claves[0]))

	require.False(t, dic.Pertenece(claves[1]))
	require.False(t, dic.Pertenece(claves[2]))
	dic.Guardar(claves[1], valores[1])
	require.True(t, dic.Pertenece(claves[0]))
	require.True(t, dic.Pertenece(claves[1]))
	require.EqualValues(t, 2, dic.Cantidad())
	require.EqualValues(t, valores[0], dic.Obtener(claves[0]))
	require.EqualValues(t, valores[1], dic.Obtener(claves[1]))

	require.False(t, dic.Pertenece(claves[2]))
	dic.Guardar(claves[2], valores[2])
	require.True(t, dic.Pertenece(claves[0]))
	require.True(t, dic.Pertenece(claves[1]))
	require.True(t, dic.Pertenece(claves[2]))
	require.EqualValues(t, 3, dic.Cantidad())
	require.EqualValues(t, valores[0], dic.Obtener(claves[0]))
	require.EqualValues(t, valores[1], dic.Obtener(claves[1]))
	require.EqualValues(t, valores[2], dic.Obtener(claves[2]))
}

func TestReemplazoDatos(t *testing.T) {
	t.Log("Guarda un par de claves, y luego vuelve a guardar, buscando que el dato se haya reemplazado")
	clave := "Gato"
	clave2 := "Perro"
	dic := TDADiccionario.CrearABB[string, string](compStr)
	dic.Guardar(clave, "miau")
	dic.Guardar(clave2, "guau")
	require.True(t, dic.Pertenece(clave))
	require.True(t, dic.Pertenece(clave2))
	require.EqualValues(t, "miau", dic.Obtener(clave))
	require.EqualValues(t, "guau", dic.Obtener(clave2))
	require.EqualValues(t, 2, dic.Cantidad())

	dic.Guardar(clave, "miu")
	dic.Guardar(clave2, "baubau")
	require.True(t, dic.Pertenece(clave))
	require.True(t, dic.Pertenece(clave2))
	require.EqualValues(t, 2, dic.Cantidad())
	require.EqualValues(t, "miu", dic.Obtener(clave))
	require.EqualValues(t, "baubau", dic.Obtener(clave2))
}

func TestReemplazoDatosHopscotch(t *testing.T) {
	t.Log("Guarda bastantes claves, y luego reemplaza sus datos. Luego valida que todos los datos sean " +
		"correctos. Para una implementación Hopscotch, detecta errores al hacer lugar o guardar elementos.")

	dic := TDADiccionario.CrearABB[int, int](compNums)
	for i := 0; i < 500; i++ {
		dic.Guardar(i, i)
	}
	for i := 0; i < 500; i++ {
		dic.Guardar(i, 2*i)
	}
	ok := true
	for i := 0; i < 500 && ok; i++ {
		ok = dic.Obtener(i) == 2*i
	}
	require.True(t, ok, "Los elementos no fueron actualizados correctamente")
}

func TestDiccBorrar(t *testing.T) {
	t.Log("Guarda algunos pocos elementos en el ABB, y se los borra, revisando que en todo momento " +
		"el ABB se comporte de manera adecuada")
	clave1 := "Gato"
	clave2 := "Perro"
	clave3 := "Vaca"
	valor1 := "miau"
	valor2 := "guau"
	valor3 := "moo"
	claves := []string{clave1, clave2, clave3}
	valores := []string{valor1, valor2, valor3}
	dic := TDADiccionario.CrearABB[string, string](compStr)

	require.False(t, dic.Pertenece(claves[0]))
	require.False(t, dic.Pertenece(claves[0]))
	dic.Guardar(claves[0], valores[0])
	dic.Guardar(claves[1], valores[1])
	dic.Guardar(claves[2], valores[2])

	require.True(t, dic.Pertenece(claves[2]))
	require.EqualValues(t, valores[2], dic.Borrar(claves[2]))
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Borrar(claves[2]) })
	require.EqualValues(t, 2, dic.Cantidad())
	require.False(t, dic.Pertenece(claves[2]))

	require.True(t, dic.Pertenece(claves[0]))
	require.EqualValues(t, valores[0], dic.Borrar(claves[0]))
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Borrar(claves[0]) })
	require.EqualValues(t, 1, dic.Cantidad())
	require.False(t, dic.Pertenece(claves[0]))
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Obtener(claves[0]) })

	require.True(t, dic.Pertenece(claves[1]))
	require.EqualValues(t, valores[1], dic.Borrar(claves[1]))
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Borrar(claves[1]) })
	require.EqualValues(t, 0, dic.Cantidad())
	require.False(t, dic.Pertenece(claves[1]))
	require.PanicsWithValue(t, TDADiccionario.CLAVE_VACIA, func() { dic.Obtener(claves[1]) })
}

func TestReutlizacionDeBorrado(t *testing.T) {
	t.Log("Revisa que no haya problema " +
		"reinsertando un elemento borrado")
	dic := TDADiccionario.CrearABB[string, string](compStr)
	clave := "hola"
	dic.Guardar(clave, "mundo!")
	dic.Borrar(clave)
	require.EqualValues(t, 0, dic.Cantidad())
	require.False(t, dic.Pertenece(clave))
	dic.Guardar(clave, "mundooo!")
	require.True(t, dic.Pertenece(clave))
	require.EqualValues(t, 1, dic.Cantidad())
	require.EqualValues(t, "mundooo!", dic.Obtener(clave))
}

func TestConClaveNumerica(t *testing.T) {
	t.Log("Valida que no solo funcione con strings")
	dic := TDADiccionario.CrearABB[int, string](compNums)
	clave := 10
	valor := "Gatito"

	dic.Guardar(clave, valor)
	require.EqualValues(t, 1, dic.Cantidad())
	require.True(t, dic.Pertenece(clave))
	require.EqualValues(t, valor, dic.Obtener(clave))
	require.EqualValues(t, valor, dic.Borrar(clave))
	require.False(t, dic.Pertenece(clave))
}

func TestClavesVacias(t *testing.T) {
	t.Log("Guardamos una clave vacía (i.e. \"\") y deberia funcionar sin problemas")
	dic := TDADiccionario.CrearABB[string, string](compStr)
	clave := ""
	dic.Guardar(clave, clave)
	require.True(t, dic.Pertenece(clave))
	require.EqualValues(t, 1, dic.Cantidad())
	require.EqualValues(t, clave, dic.Obtener(clave))
}

func TestValoresNulos(t *testing.T) {
	t.Log("Probamos que el valor puede ser nil sin problemas")
	dic := TDADiccionario.CrearABB[string, *int](compStr)
	clave := "Pez"
	dic.Guardar(clave, nil)
	require.True(t, dic.Pertenece(clave))
	require.EqualValues(t, 1, dic.Cantidad())
	require.EqualValues(t, (*int)(nil), dic.Obtener(clave))
	require.EqualValues(t, (*int)(nil), dic.Borrar(clave))
	require.False(t, dic.Pertenece(clave))
}

func buscarCla(clave string, claves []string) int {
	for i, c := range claves {
		if c == clave {
			return i
		}
	}
	return -1
}

func TestIteradorInternoClave(t *testing.T) {
	t.Log("Valida que todas las claves sean recorridas (y una única vez) con el iterador interno")
	clave1 := "Gato"
	clave2 := "Perro"
	clave3 := "Vaca"
	claves := []string{clave1, clave2, clave3}
	dic := TDADiccionario.CrearABB[string, *int](compStr)
	dic.Guardar(claves[0], nil)
	dic.Guardar(claves[1], nil)
	dic.Guardar(claves[2], nil)

	cs := []string{"", "", ""}
	cantidad := 0
	cantPtr := &cantidad

	dic.Iterar(func(clave string, dato *int) bool {
		cs[cantidad] = clave
		*cantPtr = *cantPtr + 1
		return true
	})

	require.EqualValues(t, 3, cantidad)
	require.NotEqualValues(t, -1, buscarCla(cs[0], claves))
	require.NotEqualValues(t, -1, buscarCla(cs[1], claves))
	require.NotEqualValues(t, -1, buscarCla(cs[2], claves))
	require.NotEqualValues(t, cs[0], cs[1])
	require.NotEqualValues(t, cs[0], cs[2])
	require.NotEqualValues(t, cs[2], cs[1])
}

func TestIteradorInternoValor(t *testing.T) {
	t.Log("Valida que los datos sean recorridas correctamente (y una única vez) con el iterador interno")
	clave1 := "Gato"
	clave2 := "Perro"
	clave3 := "Vaca"
	clave4 := "Burrito"
	clave5 := "Hamster"

	dic := TDADiccionario.CrearABB[string, int](compStr)
	dic.Guardar(clave1, 6)
	dic.Guardar(clave2, 2)
	dic.Guardar(clave3, 3)
	dic.Guardar(clave4, 4)
	dic.Guardar(clave5, 5)

	factorial := 1
	ptrFactorial := &factorial
	dic.Iterar(func(_ string, dato int) bool {
		*ptrFactorial *= dato
		return true
	})

	require.EqualValues(t, 720, factorial)
}

func generarNumeroAleatorio(N, L int) TDADiccionario.Diccionario[int, int] {
	rand.Seed(time.Now().UnixNano())
	res := TDADiccionario.CrearHash[int, int]()
	for res.Cantidad() != L {
		i := rand.Intn(N)
		res.Guardar(i, i)
	}
	return res
}

func ejecutarPruebasVolumen(b *testing.B, n int) {
	dic := TDADiccionario.CrearABB[string, int](compStr)

	claves := make([]string, n)
	valores := make([]int, n)
	x := generarNumeroAleatorio(10000000, n)
	iter := x.Iterador()
	cont := 0
	for iter.HaySiguiente() {
		i, _ := iter.VerActual()
		valores[cont] = i
		claves[cont] = fmt.Sprintf("%08d", i)
		dic.Guardar(claves[cont], valores[cont])
		cont++
		iter.Siguiente()
	}

	require.EqualValues(b, n, dic.Cantidad(), "La cantidad de elementos es incorrecta")

	/* Verifica que devuelva los valores correctos */
	ok := true
	for i := 0; i < n; i++ {
		ok = dic.Pertenece(claves[i])
		if !ok {
			break
		}
		ok = dic.Obtener(claves[i]) == valores[i]
		if !ok {
			break
		}
	}

	require.True(b, ok, "Pertenece y Obtener con muchos elementos no funciona correctamente")
	require.EqualValues(b, n, dic.Cantidad(), "La cantidad de elementos es incorrecta")

	/* Verifica que borre y devuelva los valores correctos */
	for i := 0; i < n; i++ {
		ok = dic.Borrar(claves[i]) == valores[i]
		if !ok {
			break
		}
		ok = !dic.Pertenece(claves[i])
		if !ok {
			break
		}
	}

	require.True(b, ok, "Borrar muchos elementos no funciona correctamente")
	require.EqualValues(b, 0, dic.Cantidad())
}

func BenchmarkDicc(b *testing.B) {
	b.Log("Prueba de stress del ABB. Prueba guardando distinta cantidad de elementos (muy grandes), " +
		"ejecutando muchas veces las pruebas para generar un benchmark. Valida que la cantidad " +
		"sea la adecuada. Luego validamos que podemos obtener y ver si pertenece cada una de las claves geeneradas, " +
		"y que luego podemos borrar sin problemas")
	for _, n := range TAM_VOLUMEN {
		b.Run(fmt.Sprintf("Prueba %d elementos", n), func(b *testing.B) {
			for i := 0; i < b.N; i++ {
				ejecutarPruebasVolumen(b, n)
			}
		})
	}
}

func TestIterarDiccVacio(t *testing.T) {
	t.Log("Iterar sobre Dicc vacio es simplemente tenerlo al final")
	dic := TDADiccionario.CrearABB[string, int](compStr)
	iter := dic.Iterador()
	require.False(t, iter.HaySiguiente())
	require.PanicsWithValue(t, TDADiccionario.ITER_VACIO, func() { iter.VerActual() })
	require.PanicsWithValue(t, TDADiccionario.ITER_VACIO, func() { iter.Siguiente() })
}

func TestDiccIterar(t *testing.T) {
	t.Log("Guardamos 3 valores en un ABB, e iteramos validando que las claves sean todas diferentes " +
		"pero pertenecientes al ABB. Además los valores de VerActual y Siguiente van siendo correctos entre sí")
	clave1 := "Gato"
	clave2 := "Perro"
	clave3 := "Vaca"
	valor1 := "miau"
	valor2 := "guau"
	valor3 := "moo"
	claves := []string{clave1, clave2, clave3}
	valores := []string{valor1, valor2, valor3}
	dic := TDADiccionario.CrearABB[string, string](compStr)
	dic.Guardar(claves[0], valores[0])
	dic.Guardar(claves[1], valores[1])
	dic.Guardar(claves[2], valores[2])
	iter := dic.Iterador()

	require.True(t, iter.HaySiguiente())
	primero, _ := iter.VerActual()
	require.NotEqualValues(t, -1, buscarCla(primero, claves))

	iter.Siguiente()
	segundo, segundo_valor := iter.VerActual()
	require.NotEqualValues(t, -1, buscarCla(segundo, claves))
	require.EqualValues(t, valores[buscarCla(segundo, claves)], segundo_valor)
	require.NotEqualValues(t, primero, segundo)
	require.True(t, iter.HaySiguiente())

	iter.Siguiente()
	require.True(t, iter.HaySiguiente())
	tercero, _ := iter.VerActual()
	require.NotEqualValues(t, -1, buscarCla(tercero, claves))
	require.NotEqualValues(t, primero, tercero)
	require.NotEqualValues(t, segundo, tercero)
	iter.Siguiente()

	require.False(t, iter.HaySiguiente())
	require.PanicsWithValue(t, TDADiccionario.ITER_VACIO, func() { iter.VerActual() })
	require.PanicsWithValue(t, TDADiccionario.ITER_VACIO, func() { iter.Siguiente() })
}

func TestIteradorNoLlegaFinal(t *testing.T) {
	t.Log("Crea un iterador y no lo avanza. Luego crea otro iterador y lo avanza.")
	dic := TDADiccionario.CrearABB[string, string](compStr)
	claves := []string{"A", "B", "C"}
	dic.Guardar(claves[0], "")
	dic.Guardar(claves[1], "")
	dic.Guardar(claves[2], "")

	dic.Iterador()
	iter2 := dic.Iterador()
	iter2.Siguiente()
	iter3 := dic.Iterador()
	primero, _ := iter3.VerActual()
	iter3.Siguiente()
	segundo, _ := iter3.VerActual()
	iter3.Siguiente()
	tercero, _ := iter3.VerActual()
	iter3.Siguiente()
	require.False(t, iter3.HaySiguiente())
	require.NotEqualValues(t, primero, segundo)
	require.NotEqualValues(t, tercero, segundo)
	require.NotEqualValues(t, primero, tercero)
	require.NotEqualValues(t, -1, buscarCla(primero, claves))
	require.NotEqualValues(t, -1, buscarCla(segundo, claves))
	require.NotEqualValues(t, -1, buscarCla(tercero, claves))
}

func ejecutarPruebaVolumenIterador(b *testing.B, n int) {
	dic := TDADiccionario.CrearABB[string, *int](compStr)

	claves := make([]string, n)
	valores := make([]int, n)

	x := generarNumeroAleatorio(10000000, n)
	itera := x.Iterador()
	cont := 0

	for itera.HaySiguiente() {
		i, _ := itera.VerActual()
		valores[cont] = i
		claves[cont] = fmt.Sprintf("%08d", i)
		dic.Guardar(claves[cont], &valores[cont])
		cont++
		itera.Siguiente()
	}

	// Prueba de iteración sobre las claves almacenadas.
	iter := dic.Iterador()
	require.True(b, iter.HaySiguiente())

	ok := true
	var i int
	var clave string
	var valor *int

	for i = 0; i < n; i++ {
		if !iter.HaySiguiente() {
			ok = false
			break
		}
		c1, v1 := iter.VerActual()
		clave = c1
		if clave == "" {
			ok = false
			break
		}
		valor = v1
		if valor == nil {
			ok = false
			break
		}
		*valor = n
		iter.Siguiente()
	}
	require.True(b, ok, "Iteracion en volumen no funciona correctamente")
	require.EqualValues(b, n, i, "No se recorrió todo el largo")
	require.False(b, iter.HaySiguiente(), "El iterador debe estar al final luego de recorrer")

	ok = true
	for i = 0; i < n; i++ {
		if valores[i] != n {
			ok = false
			break
		}
	}
	require.True(b, ok, "No se cambiaron todos los elementos")
}

func BenchmarkIteradorExt(b *testing.B) {
	b.Log("Prueba de stress del Iterador del ABB. Prueba guardando distinta cantidad de elementos " +
		"(muy grandes) b.N elementos, iterarlos todos sin problemas. Se ejecuta cada prueba b.N veces para generar " +
		"un benchmark")
	for _, n := range TAM_VOLUMEN {
		b.Run(fmt.Sprintf("Prueba %d elementos", n), func(b *testing.B) {
			for i := 0; i < b.N; i++ {
				ejecutarPruebaVolumenIterador(b, n)
			}
		})
	}
}

func TestVolumenIteradorCortes(t *testing.T) {
	t.Log("Prueba de volumen de iterador interno, para validar que siempre que se indique que se corte" +
		" la iteración con la función visitar, se corte")

	dic := TDADiccionario.CrearABB[int, int](compNums)

	for i := 0; i < 10000; i++ {
		dic.Guardar(i, i)
	}

	seguirEjecutando := true
	siguioEjecutandoCuandoNoDebia := false

	dic.Iterar(func(c int, v int) bool {
		if !seguirEjecutando {
			siguioEjecutandoCuandoNoDebia = true
			return false
		}
		if c%100 == 0 {
			seguirEjecutando = false
			return false
		}
		return true
	})

	require.False(t, seguirEjecutando, "Se tendría que haber encontrado un elemento que genere el corte")
	require.False(t, siguioEjecutandoCuandoNoDebia,
		"No debería haber seguido ejecutando si encontramos un elemento que hizo que la iteración corte")
}

func TestIterarRangoCompleto(t *testing.T) {
	t.Log("Prueba que IterarRango con hasta = desde = nil" +
		" se comporte como iterador interno de diccionario")
	clave1 := "Gato"
	clave2 := "Perro"
	clave3 := "Vaca"
	claves := []string{clave1, clave2, clave3}
	dic := TDADiccionario.CrearABB[string, *int](compStr)
	dic.Guardar(claves[0], nil)
	dic.Guardar(claves[1], nil)
	dic.Guardar(claves[2], nil)

	cs := []string{"", "", ""}
	cantidad := 0
	cantPtr := &cantidad

	dic.IterarRango(nil, nil, func(clave string, dato *int) bool {
		cs[cantidad] = clave
		*cantPtr = *cantPtr + 1
		return true
	})

	require.EqualValues(t, 3, cantidad)
	require.NotEqualValues(t, -1, buscarCla(cs[0], claves))
	require.NotEqualValues(t, -1, buscarCla(cs[1], claves))
	require.NotEqualValues(t, -1, buscarCla(cs[2], claves))
	require.NotEqualValues(t, cs[0], cs[1])
	require.NotEqualValues(t, cs[0], cs[2])
	require.NotEqualValues(t, cs[2], cs[1])
}

func TestIterarRangoSinDesde(t *testing.T) {
	t.Log("Prueba que IterarRango con desde = nil" +
		" se comporte correctamente")

	dic := TDADiccionario.CrearABB[int, int](compNums)
	dic.Guardar(6, 6)
	dic.Guardar(2, 2)
	dic.Guardar(3, 3)
	dic.Guardar(9, 9)
	dic.Guardar(4, 4)
	dic.Guardar(5, 5)
	dic.Guardar(8, 8)
	hasta := 7
	factorial := 1
	ptrFactorial := &factorial
	dic.IterarRango(nil, &hasta, func(_ int, dato int) bool {
		*ptrFactorial *= dato
		return true
	})

	require.EqualValues(t, 720, factorial)
}

func TestIterarRangoSinHasta(t *testing.T) {
	t.Log("Prueba que IterarRango con hasta = nil" +
		" se comporte correctamente")

	dic := TDADiccionario.CrearABB[int, int](compNums)
	dic.Guardar(6, 6)
	dic.Guardar(2, 2)
	dic.Guardar(3, 3)
	dic.Guardar(0, 0)
	dic.Guardar(4, 4)
	dic.Guardar(5, 5)
	dic.Guardar(1, 1)
	desde := 2
	factorial := 1
	ptrFactorial := &factorial
	dic.IterarRango(&desde, nil, func(_ int, dato int) bool {
		*ptrFactorial *= dato
		return true
	})

	require.EqualValues(t, 720, factorial)
}

func TestIterarRangos(t *testing.T) {
	t.Log("Prueba que IterarRango entre rangos" +
		" se comporte correctamente")

	dic := TDADiccionario.CrearABB[int, int](compNums)
	dic.Guardar(6, 6)
	dic.Guardar(7, 7)
	dic.Guardar(2, 2)
	dic.Guardar(3, 3)
	dic.Guardar(0, 0)
	dic.Guardar(9, 9)
	dic.Guardar(4, 4)
	dic.Guardar(5, 5)
	dic.Guardar(123, 123)
	dic.Guardar(1, 1)
	desde := 2
	hasta := 6
	factorial := 1
	ptrFactorial := &factorial
	dic.IterarRango(&desde, &hasta, func(_ int, dato int) bool {
		*ptrFactorial *= dato
		return true
	})

	require.EqualValues(t, 720, factorial)
}

func TestIteradorRangoDiccVacio(t *testing.T) {
	t.Log("IteradorRango sobre Arbol vacio es simplemente tenerlo al final")
	dic := TDADiccionario.CrearABB[string, int](compStr)
	iter := dic.IteradorRango(nil, nil)
	require.False(t, iter.HaySiguiente())
	require.PanicsWithValue(t, TDADiccionario.ITER_VACIO, func() { iter.VerActual() })
	require.PanicsWithValue(t, TDADiccionario.ITER_VACIO, func() { iter.Siguiente() })
}

func TestDiccIteradorRangoCompleto(t *testing.T) {
	t.Log("Comprueba que el IteradorRango con desde = hasta = nil se comporta como el Iterador")
	clave1 := "Gato"
	clave2 := "Perro"
	clave3 := "Vaca"
	valor1 := "miau"
	valor2 := "guau"
	valor3 := "moo"
	claves := []string{clave1, clave2, clave3}
	valores := []string{valor1, valor2, valor3}
	dic := TDADiccionario.CrearABB[string, string](compStr)
	dic.Guardar(claves[0], valores[0])
	dic.Guardar(claves[1], valores[1])
	dic.Guardar(claves[2], valores[2])
	iter := dic.IteradorRango(nil, nil)

	require.True(t, iter.HaySiguiente())
	primero, _ := iter.VerActual()
	require.NotEqualValues(t, -1, buscarCla(primero, claves))

	iter.Siguiente()
	segundo, segundo_valor := iter.VerActual()
	require.NotEqualValues(t, -1, buscarCla(segundo, claves))
	require.EqualValues(t, valores[buscarCla(segundo, claves)], segundo_valor)
	require.NotEqualValues(t, primero, segundo)
	require.True(t, iter.HaySiguiente())

	iter.Siguiente()
	require.True(t, iter.HaySiguiente())
	tercero, _ := iter.VerActual()
	require.NotEqualValues(t, -1, buscarCla(tercero, claves))
	require.NotEqualValues(t, primero, tercero)
	require.NotEqualValues(t, segundo, tercero)
	iter.Siguiente()

	require.False(t, iter.HaySiguiente())
	require.PanicsWithValue(t, TDADiccionario.ITER_VACIO, func() { iter.VerActual() })
	require.PanicsWithValue(t, TDADiccionario.ITER_VACIO, func() { iter.Siguiente() })
}

func TestIteradorRangoSinHasta(t *testing.T) {
	t.Log("Prueba que IteradorRango con hasta = nil" +
		" se comporte correctamente")
	abb := TDADiccionario.CrearABB[int, int](compNums)
	for i := 0; i < 11; i++ {
		abb.Guardar(i, i)
	}
	desde := 5
	cont := 0
	iter := abb.IteradorRango(&desde, nil)
	for iter.HaySiguiente() {
		k, _ := iter.VerActual()
		cont += k
		iter.Siguiente()
	}
	require.EqualValues(t, 45, cont)
}

func TestIteradorRangoSinDesde(t *testing.T) {
	t.Log("Prueba que IteradorRango con desde = nil" +
		" se comporte correctamente")
	abb := TDADiccionario.CrearABB[int, int](compNums)
	for i := 0; i < 11; i++ {
		abb.Guardar(i, i)
	}
	hasta := 5
	cont := 0
	iter := abb.IteradorRango(nil, &hasta)
	for iter.HaySiguiente() {
		k, _ := iter.VerActual()
		cont += k
		iter.Siguiente()
	}
	require.EqualValues(t, 15, cont)
}

func TestIteradorRangoDefinido(t *testing.T) {
	t.Log("Prueba que IteradorRango entre rangos" +
		" se comporte correctamente")
	abb := TDADiccionario.CrearABB[int, int](compNums)
	for i := 0; i < 11; i++ {
		abb.Guardar(i, i)
	}
	hasta := 8
	desde := 3
	cont := 0
	iter := abb.IteradorRango(&desde, &hasta)
	for iter.HaySiguiente() {
		k, _ := iter.VerActual()
		cont += k
		iter.Siguiente()
	}
	require.EqualValues(t, 33, cont)
}

func TestIteradorRangosVolumen(t *testing.T) {
	t.Log("Prueba de volumen de IteradorRango")
	abb := TDADiccionario.CrearABB[int, int](compNums)
	desde := 2
	hasta := 19998
	cont1 := 0
	for i := 0; i < 20000; i++ {
		abb.Guardar(i, i)
		if i >= desde && i <= hasta {
			cont1 += i
		}
	}
	cont2 := 0
	iter := abb.IteradorRango(&desde, &hasta)
	for iter.HaySiguiente() {
		clave, _ := iter.VerActual()
		cont2 += clave
		iter.Siguiente()
	}
	require.EqualValues(t, cont1, cont2)
}

func TestIterarRangosVolumen(t *testing.T) {
	t.Log("Prueba de volumen de IterarRango")
	abb := TDADiccionario.CrearABB[int, int](compNums)
	desde := 2
	hasta := 19998
	cont1 := 0
	for i := 0; i < 20000; i++ {
		abb.Guardar(i, i)
		if i >= desde && i <= hasta {
			cont1 += i
		}
	}
	cont2 := 0
	abb.IterarRango(&desde, &hasta, func(clave, _ int) bool {
		cont2 += clave
		return true
	})
	require.EqualValues(t, cont1, cont2)
}
