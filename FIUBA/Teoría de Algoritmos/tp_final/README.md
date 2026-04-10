Trabajo Práctico Final

Teoría de Algoritmos 1 - 1c 2025 Trabajo Práctico Final
Lineamientos básicos

    El trabajo se realizará en grupos de cuatro o cinco personas.

    Se debe entregar el informe en formato pdf en el aula virtual de la materia.

    El informe debe presentar carátula con el nombre del grupo, datos de los integrantes y fecha de entrega. Debe incluir número de hoja en cada página. No debe superar las 30 páginas + carátula + índice + referencias.

    Al ser un trabajo de investigación debe OBLIGATORIAMENTE incluir las fuentes utilizadas. Utilizar el formato APA.

    En caso de re-entrega, entregar un apartado donde se explicitan las correcciones realizadas.

Parte 1: Personal para proyectos

Una consultora ofrece personal calificado para 3 tipos de proyectos. Cada proyecto requiere ingenieros y diseñadores. Actualmente tiene en su nómina 17 y 11 de estos profesionales respectivamente. El proyecto tipo “A” requiere 1 ingeniero y 3 diseñadores. El proyecto tipo “B” requiere 1 ingeniero y 2 diseñadores. Finalmente el proyecto tipo “C” requiere 3 y 2. Por cada proyecto gana respectivamente 200, 100 y 300 (en millones de pesos). Desean determinar cuántos proyectos y de qué tipo aceptar para maximizar las ganancias.

Se pide:

    Expresar y explicar el problema como un problema de programación lineal.

    Explicar como resolver el problema utilizando Simplex. Brindar pseudocódigo y explicación de su propuesta. Expresar como se representa la solución.

    Analizar la complejidad temporal y espacial de cada uno de los pasos de su solución.

    Presente paso a paso la solución del problema. Presente esquemáticamente cada iteración del algoritmo. Indique qué decisiones se toma en cada uno de estos y los cálculos realizados.

    Analizar la solución obtenida. ¿Corresponde a la solución óptima del problema? Según la naturaleza del problema, ¿lo puede encontrar en tiempo polinomial? Justificar.

    Investigar la aplicación de Branch and Bound dentro de programación lineal entera. Explique cómo funciona paso a paso. Brinde pseudocódigo. ¿Lo puede utilizar en el problema? En caso afirmativo desarrolle como hacerlo paso a paso.

    Programe su propuesta. Puede utilizar librerías para Simplex. (Ejemplos: ALGLIB o PulP).

Parte 2: Buscando una solución aceptable.

Para el desarrollo de un proyecto estamos buscando inversores. Contamos con una preselección de “n” de estos. cada uno de ellos nos prometió aportar cierta cantidad de dinero (este valor no necesariamente es igual para cada inversor). Nos gustaría aceptar a todos. Sin embargo, algunos inversores se niegan a participar si otros están. Nos gustaría determinar a cuáles aceptar para maximizar el dinero total para la inversión

Se pide:

    Analizar el problema y determinar si es posible resolverlo de forma eficiente.

    Proponer 2 algoritmos heurísticos/randomizados o de aproximación para resolverlo. Explicar cómo funcionan

    Brindar pseudocódigo y análisis completo del mismo (análisis de complejidad temporal, espacial, optimalidad, grado de aproximación, según corresponda al tipo de solución).

    Realizar su programa y brindar varios ejemplos para su ejecución

    Realizar un análisis empírico de sus soluciones. ¿Puede determinar en qué casos es mejor uno que el otro?

Parte 3: Autómatas finitos

Los siguientes lenguajes corresponden a la intersección (expresado mediante la conjunción “y”) de dos lenguajes más simples (los símbolos de los mismos corresponden a los números 0 y 1) :

lenguaje "a": {w| w (tiene dentro suyo la subcadena “1011”) y (tiene un número par de “0”) }
lenguaje "b": {w| w (toda posición impar es un “1”) y (termina con 3 “1”)}

Ejemplos:

a: “101110”, “1010111”
b: “1010111”, “101010111”

Se pide:

    Construir un autómata finito determinista (AFD) de forma formal para cada uno de los lenguajes simples.

    Basándose en los autómatas construidos generar de forma formal los dos autómatas finitos determinísticos de los lenguajes más complejos.

    Representar cada uno de los AFD mediante su representación gráfica

    Para cada AFD Brindar un ejemplo de una cadena que acepta y otra que rechaza. Explicar cómo determinar su autómata si es aceptado o rechazado paso a paso.
