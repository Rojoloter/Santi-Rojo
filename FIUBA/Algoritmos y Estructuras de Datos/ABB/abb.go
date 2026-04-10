package diccionario

import TDAPila "tdas/pila"

type funcCmp[K comparable] func(K, K) int

type nodoAbb[K comparable, V any] struct {
	izquierdo *nodoAbb[K, V]
	derecho   *nodoAbb[K, V]
	clave     K
	dato      V
}

type abb[K comparable, V any] struct {
	raiz     *nodoAbb[K, V]
	cantidad int
	cmp      funcCmp[K]
}

func crearNodoABB[K comparable, V any]() *nodoAbb[K, V] {
	nodo := new(nodoAbb[K, V])
	return nodo
}

func CrearABB[K comparable, V any](comp func(K, K) int) DiccionarioOrdenado[K, V] {
	arbol := new(abb[K, V])
	arbol.cmp = comp
	return arbol
}

func (arbol *abb[K, V]) Cantidad() int {
	return arbol.cantidad
}

func (arbol *abb[K, V]) buscarEnArbol(clave K, nodo *nodoAbb[K, V], padre *nodoAbb[K, V]) (nodoActual, nodoAnterior *nodoAbb[K, V]) {
	if nodo == nil {
		return nil, padre
	}
	if nodo.clave == clave {
		return nodo, padre
	} else if arbol.cmp(clave, nodo.clave) > 0 {
		return arbol.buscarEnArbol(clave, nodo.derecho, nodo)
	}
	return arbol.buscarEnArbol(clave, nodo.izquierdo, nodo)
}

func (arbol *abb[K, V]) Pertenece(clave K) bool {
	nodo, _ := arbol.buscarEnArbol(clave, arbol.raiz, nil)
	return nodo != nil
}

func (arbol *abb[K, V]) Obtener(clave K) V {
	nodo, _ := arbol.buscarEnArbol(clave, arbol.raiz, nil) // No reutilizamos el pertenece porque entonces estaríamos haciendo la busqueda del nodo dos veces
	if nodo == nil {
		panic(CLAVE_VACIA)
	}
	return nodo.dato
}

func (arbol *abb[K, V]) guardarNodo(nodoAGuardar *nodoAbb[K, V]) bool {
	nodo, padre := arbol.buscarEnArbol(nodoAGuardar.clave, arbol.raiz, nil)
	if nodo != nil {
		nodo.dato = nodoAGuardar.dato
		return false
	} else {
		if padre == nil {
			arbol.raiz = nodoAGuardar
		} else if arbol.cmp(padre.clave, nodoAGuardar.clave) > 0 {
			padre.izquierdo = nodoAGuardar
		} else {
			padre.derecho = nodoAGuardar
		}
	}
	return true
}

func (arbol *abb[K, V]) Guardar(clave K, dato V) {
	nodo := crearNodoABB[K, V]()
	nodo.clave = clave
	nodo.dato = dato
	if arbol.guardarNodo(nodo) {
		arbol.cantidad++
	}
}

func (arbol *abb[K, V]) Borrar(clave K) V {
	nodo, padre := arbol.buscarEnArbol(clave, arbol.raiz, nil)
	if nodo == nil {
		panic(CLAVE_VACIA)
	}
	res := nodo.dato
	hijoIzq := nodo.izquierdo
	hijoDer := nodo.derecho

	if hijoIzq == nil && hijoDer == nil { // Se borra una hoja
		if padre == nil {
			arbol.raiz = nil
		} else if arbol.cmp(clave, padre.clave) < 0 {
			padre.izquierdo = nil
		} else {
			padre.derecho = nil
		}
	} else if (hijoIzq != nil && hijoDer == nil) || (hijoIzq == nil && hijoDer != nil) { // Se borra un nodo con un solo hijo
		if hijoIzq != nil {
			if padre == nil {
				arbol.raiz = hijoIzq
			} else if arbol.cmp(clave, padre.clave) < 0 {
				padre.izquierdo = hijoIzq
			} else {
				padre.derecho = hijoIzq
			}
		} else {
			if padre == nil {
				arbol.raiz = hijoDer
			} else if arbol.cmp(clave, padre.clave) < 0 {
				padre.izquierdo = hijoDer
			} else {
				padre.derecho = hijoDer
			}
		}
	} else { // Se borra un nodo con dos hijos
		reemp := arbol.reemplazo(*nodo.derecho)
		arbol.Borrar(reemp.clave)
		nodo.clave = reemp.clave
		nodo.dato = reemp.dato
		arbol.cantidad++ //La llamada recursiva de arriba resta uno mas de lo que debería
	}
	arbol.cantidad--
	return res
}

func (arbol *abb[K, V]) reemplazo(nodo nodoAbb[K, V]) nodoAbb[K, V] {
	if nodo.izquierdo == nil {
		return nodo
	}
	return arbol.reemplazo(*nodo.izquierdo)
}

func (arbol *abb[K, V]) IterarRango(desde *K, hasta *K, visitar func(clave K, dato V) bool) {
	arbol.auxIterarRango(arbol.raiz, desde, hasta, visitar)
}

func (arbol *abb[K, V]) auxIterarRango(nodo *nodoAbb[K, V], desde *K, hasta *K, visitar func(clave K, dato V) bool) bool {
	if nodo == nil {
		return false
	}

	if hasta != nil && arbol.cmp(nodo.clave, *hasta) > 0 {
		return arbol.auxIterarRango(nodo.izquierdo, desde, hasta, visitar)
	} else if desde != nil && arbol.cmp(nodo.clave, *desde) < 0 {
		return arbol.auxIterarRango(nodo.derecho, desde, hasta, visitar)
	} else {
		corteIzq := arbol.auxIterarRango(nodo.izquierdo, desde, hasta, visitar)
		if corteIzq || !visitar(nodo.clave, nodo.dato) {
			return true
		}
		corteDer := arbol.auxIterarRango(nodo.derecho, desde, hasta, visitar)
		if corteDer {
			return true
		}
	}
	return false
}

func (arbol *abb[K, V]) Iterar(visitar func(clave K, dato V) bool) {
	arbol.IterarRango(nil, nil, visitar)
}

type iterDiccionarioOrdenado[K comparable, V any] struct {
	pila  TDAPila.Pila[*nodoAbb[K, V]]
	desde *K
	hasta *K
	arbol *abb[K, V]
}

func (arbol *abb[K, V]) IteradorRango(desde *K, hasta *K) IterDiccionario[K, V] {
	iter := new(iterDiccionarioOrdenado[K, V])
	iter.pila = TDAPila.CrearPilaDinamica[*nodoAbb[K, V]]()
	iter.desde = desde
	iter.hasta = hasta
	iter.arbol = arbol
	iter.apilarEnRango(iter.pila, desde, hasta, arbol.raiz)
	return iter
}

func (iter iterDiccionarioOrdenado[K, V]) apilarEnRango(pila TDAPila.Pila[*nodoAbb[K, V]], desde *K, hasta *K, nodo *nodoAbb[K, V]) {
	if nodo == nil {
		return
	}
	if desde == nil || iter.arbol.cmp(nodo.clave, *desde) >= 0 {
		if hasta == nil || iter.arbol.cmp(nodo.clave, *hasta) <= 0 {
			pila.Apilar(nodo)
		}
		iter.apilarEnRango(pila, desde, hasta, nodo.izquierdo)
	} else {
		iter.apilarEnRango(pila, desde, hasta, nodo.derecho)
	}
}

func (iter iterDiccionarioOrdenado[K, V]) HaySiguiente() bool {
	return !iter.pila.EstaVacia()
}

func (iter iterDiccionarioOrdenado[K, V]) VerActual() (K, V) {
	if !iter.HaySiguiente() {
		panic(ITER_VACIO)
	}
	return iter.pila.VerTope().clave, iter.pila.VerTope().dato
}

func (iter iterDiccionarioOrdenado[K, V]) Siguiente() {
	if !iter.HaySiguiente() {
		panic(ITER_VACIO)
	}
	desapilado := iter.pila.Desapilar()
	if desapilado.derecho != nil && (iter.hasta == nil || iter.arbol.cmp(desapilado.derecho.clave, *iter.hasta) <= 0) {
		iter.apilarEnRango(iter.pila, iter.desde, iter.hasta, desapilado.derecho)
	} else if desapilado.derecho != nil && desapilado.derecho.izquierdo != nil {
		iter.apilarEnRango(iter.pila, iter.desde, iter.hasta, desapilado.derecho.izquierdo)
	}
}

func (arbol *abb[K, V]) Iterador() IterDiccionario[K, V] {
	return arbol.IteradorRango(nil, nil)
}
