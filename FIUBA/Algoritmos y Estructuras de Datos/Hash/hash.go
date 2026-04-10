package diccionario

import (
	"fmt"
	TDALista "tdas/lista"
)

const (
	TAMAÑO_INICIAL       = 5
	REDIMENSION_ACHICAR  = 2
	REDIMENSION_AGRANDAR = 3
	POSICION_INICIAL     = -1
	CLAVE_VACIA          = "La clave no pertenece al diccionario"
	ITER_VACIO           = "El iterador termino de iterar"
)

type parClaveValor[K comparable, V any] struct {
	clave K
	dato  V
}

type hashAbierto[K comparable, V any] struct {
	tabla    []TDALista.Lista[*parClaveValor[K, V]]
	tam      int
	cantidad int
}

func CrearHash[K comparable, V any]() Diccionario[K, V] {
	hash := new(hashAbierto[K, V])
	hash.tam = TAMAÑO_INICIAL
	hash.tabla = make([]TDALista.Lista[*parClaveValor[K, V]], hash.tam)
	for i := 0; i < TAMAÑO_INICIAL; i++ {
		hash.tabla[i] = TDALista.CrearListaEnlazada[*parClaveValor[K, V]]()
	}
	return hash
}

func (hash *hashAbierto[K, V]) Cantidad() int {
	return hash.cantidad
}

func (hash *hashAbierto[K, V]) redimensionar(nueva_capacidad int) {
	nueva_tabla := make([]TDALista.Lista[*parClaveValor[K, V]], nueva_capacidad)
	hash.tam = nueva_capacidad
	for i := 0; i < nueva_capacidad; i++ {
		nueva_tabla[i] = TDALista.CrearListaEnlazada[*parClaveValor[K, V]]()
	}
	for _, lista := range hash.tabla {
		lista.Iterar(func(pcv *parClaveValor[K, V]) bool {
			clave := pcv.clave
			hash_conv := int(jenkins_hash(convertirABytes(clave)))
			nueva_tabla[hash_conv%hash.tam].InsertarUltimo(pcv)
			return true
		})
	}
	hash.tabla = nueva_tabla
}

func (hash *hashAbierto[K, V]) Guardar(clave K, dato V) {
	if hash.cantidad/hash.tam > REDIMENSION_AGRANDAR {
		hash.redimensionar(hash.tam * 2)
	}
	hash_conv := int(jenkins_hash(convertirABytes(clave)))
	tupla := new(parClaveValor[K, V])
	tupla.clave = clave
	tupla.dato = dato
	iter, esta_en_hash := hash.buscarEnHash(clave)
	if !esta_en_hash {
		hash.tabla[hash_conv%hash.tam].InsertarUltimo(tupla)
		hash.cantidad++
	} else {
		actual := iter.VerActual()
		actual.dato = dato
	}

}

func (hash *hashAbierto[K, V]) buscarEnHash(clave K) (TDALista.IteradorLista[*parClaveValor[K, V]], bool) {
	buscar_clave := int(jenkins_hash(convertirABytes(clave)))
	if hash.tabla[buscar_clave%hash.tam].EstaVacia() {
		return nil, false
	}
	iter := hash.tabla[buscar_clave%hash.tam].Iterador()
	for iter.HaySiguiente() {
		actual := iter.VerActual()
		if actual.clave == clave {
			return iter, true
		}
		iter.Siguiente()
	}
	return iter, false
}

func (hash *hashAbierto[K, V]) Pertenece(clave K) bool {
	_, res := hash.buscarEnHash(clave)
	return res
}

func (hash *hashAbierto[K, V]) Obtener(clave K) V {
	iter, esta_en_hash := hash.buscarEnHash(clave)
	if !esta_en_hash {
		panic(CLAVE_VACIA)
	}
	return iter.VerActual().dato
}

func (hash *hashAbierto[K, V]) Borrar(clave K) V {
	if hash.cantidad/hash.tam < REDIMENSION_ACHICAR && hash.tam > TAMAÑO_INICIAL {
		hash.redimensionar(hash.tam / 2)
	}
	iter, esta_en_hash := hash.buscarEnHash(clave)
	if !esta_en_hash {
		panic(CLAVE_VACIA)
	}
	borrar := iter.Borrar()
	hash.cantidad--
	return borrar.dato
}

func (hash *hashAbierto[K, V]) Iterar(visitar func(clave K, dato V) bool) {
	for i := 0; i < hash.tam; i++ {
		hash.tabla[i].Iterar(func(pcv *parClaveValor[K, V]) bool {
			return visitar(pcv.clave, pcv.dato)
		})
	}
}

type iteradorDicc[K comparable, V any] struct {
	tabla             *hashAbierto[K, V]
	act               *parClaveValor[K, V]
	indiceListaActual int
	iterListaActual   TDALista.IteradorLista[*parClaveValor[K, V]]
}

func (hash hashAbierto[K, V]) posicionTabla(posicion int) int {
	if posicion > hash.tam {
		return posicion
	}
	for i := 0; i < hash.tam; i++ {
		if i <= posicion {
			continue
		}
		if !hash.tabla[i].EstaVacia() {
			return i
		}
	}
	return posicion
}

func (hash *hashAbierto[K, V]) Iterador() IterDiccionario[K, V] {
	iterador := new(iteradorDicc[K, V])
	iterador.tabla = hash
	posicion := hash.posicionTabla(POSICION_INICIAL)
	if posicion == POSICION_INICIAL {
		return iterador
	}
	iterador.indiceListaActual = posicion
	iterador.iterListaActual = hash.tabla[posicion].Iterador()
	iterador.act = hash.tabla[posicion].VerPrimero()
	return iterador
}

func (iter *iteradorDicc[K, V]) HaySiguiente() bool {
	return iter.act != nil
}

func (iter *iteradorDicc[K, V]) Siguiente() {
	if !iter.HaySiguiente() {
		panic(ITER_VACIO)
	}
	iter.iterListaActual.Siguiente()
	if !iter.iterListaActual.HaySiguiente() {
		posicionActual := iter.tabla.posicionTabla(iter.indiceListaActual)
		if posicionActual == iter.indiceListaActual {
			iter.act = nil
		} else {
			iter.indiceListaActual = posicionActual
			iter.iterListaActual = iter.tabla.tabla[iter.indiceListaActual].Iterador()
			iter.act = iter.tabla.tabla[iter.indiceListaActual].VerPrimero()
		}
	} else {
		iter.act = iter.iterListaActual.VerActual()
	}
}

func (iter *iteradorDicc[K, V]) VerActual() (K, V) {
	if !iter.HaySiguiente() {
		panic(ITER_VACIO)
	}
	tupla := iter.iterListaActual.VerActual()
	return tupla.clave, tupla.dato
}

func jenkins_hash(key []byte) (hash uint32) {
	hash = 0
	for _, ch := range key {
		hash += uint32(ch)
		hash += hash << 10
		hash ^= hash >> 6
	}

	hash += hash << 3
	hash ^= hash >> 11
	hash += hash << 15

	return
}

func convertirABytes[K comparable](clave K) []byte {
	return []byte(fmt.Sprintf("%v", clave))
}
