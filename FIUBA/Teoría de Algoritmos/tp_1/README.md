Trabajo Práctico n.º 1

Teoría de Algoritmos - 1c 2025 Trabajo Práctico 1
Lineamientos básicos

    El trabajo se realizará en grupos de cinco personas.

    Se debe entregar el informe en formato pdf y código fuente en (.zip) en el aula virtual de la materia.

    El lenguaje de implementación es libre. Recomendamos utilizar C, C++ o Python. Sin embargo si se desea utilizar algún otro, se debe pactar con los docentes.

    Incluir en el informe los requisitos y procedimientos para su compilación y ejecución. La ausencia de esta información no permite probar el trabajo y deberá ser re-entregado con esta información.

    El informe debe presentar carátula con el nombre del grupo, datos de los integrantes, fecha y número de entrega. Debe incluir número de hoja en cada página. No debe superar las 25 páginas + carátula + índice + referencias.

    Debe entregar en el informe las fuentes consultadas en una sección de referencias.

    En caso de re-entrega, entregar luego del informe original un apartado con las correcciones realizadas

Parte 1: Solitario… en grupo.

Considerar el problema “Jugando al solitario” en el trabajo práctico 0. Cada participante del grupo elaboró una propuesta algorítmica al problema. Deben compararlas y responder las consignas justificando.

Se pide:

    ¿Todas las propuestas fueron greedy?

    ¿Cuáles fueron las complejidades de cada una de ellas? ¿Podemos encontrar entre ellas mejores y peores?

    Fueron todas óptimas? En caso negativo, brinde un contraejemplo para las que no. Y realice la demostración de optimalidad para una de las que sí. (si ninguna fue óptima, deben proponer una que lo sea)

Parte 2: Los puentes que se cruzan

Un rio navegable separa a una ciudad en dos regiones: norte y sur. La ciudad tiene “2n” barrios. Exactamente hay “n” barrios en cada margen. La municipalidad quiere mejorar la conectividad construyendo puentes. Cada puente debe unir un barrio del norte con uno del sur. Las propuestas de construcción son realizadas por las comunas de cada barrio. Cada barrio solo puede ser parte de una única propuesta. El comité de evaluación recibe las propuestas y debe determinar la factibilidad de la construcción del conjunto de puentes. Decimos que no es factible si existen puentes que se cruzan. En caso de no ser posible debe informar cuantos cruces de puentes existen.

Tenemos como información el orden de los barrios en cada una de las márgenes. Cada propuesta está conformada por la dupla (nombre barrio norte, nombre barrio sur).

Se pide:

    Presentar una propuesta mediante división y conquista que resuelva este problema.

    Brindar la ecuación de recurrencia y obtener su complejidad mediante el teorema maestro.

    Presentar pseudocódigo.

    Brindar un ejemplo de funcionamiento.

    Presentar un programa en python que resuelva el problema.

    Analizar: Es la complejidad de su programa igual al de su propuesta. Justifique.

Formato de los archivos:

El archivo a ejecutar se debe llamar “puentes_dq.py”

Debe recibir por parámetro el nombre de un archivo que contenga el nombre de los barrios ordenados y un segundo archivo con las propuestas.

El formato del archivo de barrios es de texto. Una línea por barrio. Primero los del norte y luego separados por una línea vacía los del sur. Por ejemplo:

Barrancas
San Pedro
El hurón
Palo seco
Puente viejo

Cienagas
Don Corleone
Barrio Este
Portuario
Torre verde

El archivo de las propuestas contiene una línea por cada propuesta. Las propuestas corresponden a un par de barrios separados por coma. Primero la del norte y luego la del sur. Ejemplo:

Puente viejo, Don Corleone
Barrancas, Cienagas
El hurón, Portuario
San Pedro, Barrio Este.
Palo seco, Torre verde.

Están todos los barrios emparejados (no hay barrios en más ni menos que en una propuesta)

La salida del programa debe ser por pantalla y solo contener un número con la cantidad de cruces.
Parte 3: Maximizando los puentes

Continuamos con la propuesta de construcción de puentes. Nos informan que debemos determinar qué puentes construir dado la propuesta evitando los cruces y maximizando la cantidad de puentes a construir.

Se pide:

    Resolver el problema utilizando programación dinámica. (incluya en su solución definición del subproblema, relación de recurrencia y pseudocódigo)

    Explique por qué su propuesta funciona.

    Analice la complejidad espacial y temporal de su propuesta.

    De un breve ejemplo paso a paso de funcionamiento de su propuesta.

    Programe su solución.

    Analice: ¿La complejidad de su propuesta es igual a la de su programa?

    Analice: ¿El resultado que retorna su programa es el único posible? De un contraejemplo si no lo es o una demostración si lo es. En caso de no serlo, ¿podrían modificar rápidamente para obtener una solución diferente?

Formato de los archivos:

El archivo a ejecutar se debe llamar “puentes_pd.py”

Debe recibir por parámetro los mismos que en el programa de división y conquista. Debe mostrar por pantalla: la cantidad de puentes que se pueden construir y los puentes seleccionados.