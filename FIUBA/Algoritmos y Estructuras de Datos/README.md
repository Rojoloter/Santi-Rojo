# TRABAJOS:
- TP0: Ejercicios introductorios para familiarizarnos con el lenguaje, Go.

- Administración de memoria: En este trabajo se simulan conceptos de manejo de memoria dinamica, ya que en el lenguaje de Go esto no es necesario, pero se consideraba necesario dar como tema.

- Pila: Implementación de un Stack, y sus respectivas pruebas.

- Cola: Implementación de una Queue, y sus respectivas pruebas.

- Lista: Implementación de una Lista Enlazada, e iteradores internos y externos, con sus respectivas pruebas.

- TP1: La consigna del TP1 era la de implementar un sistema de votación de partidos políticos dado un archivo del padrón electoral y los partidos políticos disponibles, utilizando las implementaciones hechas hasta el momento.

- Hash: implementación de un diccionario sobre una tabla de hash, y sus respectivas pruebas e iteradores. Quedaba a decisión del alumno si hacer un hash abierto o cerrado.

- ABB: implementación de un diccionario ordenado sobre un árbol binario de búsqueda, y sus respectivas pruebas e iteradores.

- Heap: implementación de una cola de prioridad sobre un heap, y sus respectivas pruebas e iteradores.

- TP2: La consigna del TP2 era la de simular una red social que dado un archivo de usuarios ya creados, permitiera loggearse, desloggearse, publicar posteos, y ver y likear posts de otros usuarios. Para esto utilizabamos las implementaciones hechas hasta ahora. 

- TP3: Este trabajo requería la implementacion de un grafo y una biblioteca genérica de funciones para grafos. Luego, usando varios articulos de wikipedia (al rededor de 75k) se debían implementar ciertas funciones que permitieran navegar entre los artículos. Están implementados:
  - una función que calcula el camino mínimo que se debe recorrer entre dos artículos, imprimendo el camino de artículos a seguir.
  - una función que imprime la cantidad de artículos que se encuentran a X distancia del artículo original.
  - una función que imprime la mayor distancia entre todos los pares de articulos disponibles, en otras palabras, el diametro del grafo.
  - una función que, dado un artículo origen, imprime el camino que se forma al seguir el primer link disponible de cada artículo, con un límite de 21 artículos.
  - una función que calcula el coeficiente de clustering de los artículos (grafo)
  - una función que recibe una lista de artículos que se quieran leer por parámetro, e imprime un orden para leerlos teniendo en cuenta que si el artículo A hace referencia al artículo B, entonces B se deberá leer antes que A.
