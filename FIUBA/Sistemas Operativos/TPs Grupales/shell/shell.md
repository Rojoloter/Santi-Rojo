# shell

### Búsqueda en $PATH
#### 1. ¿Cuáles son las diferencias entre la syscall execve(2) y la familia de wrappers proporcionados por la librería estándar de C (libc) exec(3)?

   - **execve(2)**: es la llamada al sistema del kernel, la cual hace que el programa que se ejecuta actualmente por el proceso llamador sea reemplazado por un nuevo programa, para ello requiere los siguientes argumentos:
       - ***pathname***: ruta absoluta/relativa del programa a ejecutar
       - ***argv[]***: argumentos del programa
       - ***envp[]***: variables de entorno

   - **exec(3)**: la familia de wrappers tiene como función hacer más cómodo el uso de execve, ofreciendo distintas formas de pasar parámetros o buscar el binario. Internamente, cada una prepara los parámetros adecuados y llama a execve.


    | Función    | Ruta al ejecutable                 | Manejo de entorno                                | Forma de pasar argumentos                             |
    |------------|------------------------------------|--------------------------------------------------|-------------------------------------------------------|
    | `execl()`  | Requiere ruta absoluta o relativa. | Hereda el entorno del proceso actual (`environ`).| Lista: argumentos separados por comas.                |
    | `execv()`  | Requiere ruta absoluta o relativa. | Hereda el entorno del proceso actual (`environ`).| Array `argv[]`: lista de strings terminada en `NULL`. |
    | `execle()` | Requiere ruta absoluta o relativa. | Permite especificar entorno propio con `envp[]`. | Lista + `envp[]` como último argumento.               |
    | `execlp()` | Busca el ejecutable en `$PATH`.    | Hereda el entorno del proceso actual (`environ`).| Lista: argumentos separados por comas.                |
    | `execvp()` | Busca el ejecutable en `$PATH`.    | Hereda el entorno del proceso actual (`environ`).| Array `argv[]`: lista de strings terminada en `NULL`. |
    | `execvpe()`| Busca el ejecutable en `$PATH`.    | Permite especificar entorno propio con `envp[]`. | Array `argv[]` + `envp[]`: ambos terminados en `NULL`.|
    

#### 2. ¿Puede la llamada a exec(3) fallar? ¿Cómo se comporta la implementación de la shell en ese caso?
- Si, algunos de los fallos más comunes pueden ser por memoria insuficiente (ENOMEM), archivo no ejecutable (ENOEXEC), no tener permisos de ejecución (EACCES), el binario no existe (ENOENT), demasiados argumentos (E2BIG).  
La shell indica por mensaje el tipo de error y muestra el prompt esperando otra orden. Internamente el error en exec afecta al proceso del hijo, el cual sale y devuelve 1 al padre (shell).
---

### Flujo estándar
#### Investigar el significado de 2>&1, explicar cómo funciona su forma general
a. Mostrar qué sucede con la salida de cat out.txt en el ejemplo  
b. Luego repetirlo, invirtiendo el orden de las redirecciones (es decir, 2>&1 >out.txt). ¿Cambió algo? Compararlo con el comportamiento en bash(1).

- La expresión 2>&1 indica que la salida estándar del error (stderr, descriptor 2) debe ser redirigido al mismo destino que la salida estándar (stdout, descriptor 1), es decir, los errores deben aparecer en el mismo lugar que la salida del programa.

- El error aparece en out.txt, esto se debe a que primero ocurre >out.txt entonces la salida estándar apunta a out.txt y luego con 2>&1 el error estándar es redirigido al mismo destino que la salida, el cual es out.txt. Se observa: 

<div align="center">
    <img width="70%" src="../img/shell_1.png" alt="shell1">
</div>

Comportamiento en bash:

<div align="center">
    <img width="70%" src="../img/bash_1.png" alt="bash1">
</div>
    
- Invertir el orden de las redirecciones cambia el funcionamiento, la expresión 2>&1 hace que el error estándar sea redirigido al destino de la salida, el cual apunta a la terminal y luego >out.txt redirige la salida estándar hacia out.txt. El orden de las redirecciones es importante, este comportamiento coincide con el de bash(1), el cual procesa las redirecciones en el orden que aparecen de izquierda a derecha.  
El mensaje de error se visualiza en pantalla, mientras que en la salida de cat out.txt se observa:
<div align="center">
    <img width="70%" src="../img/shell_2.png" alt="shell2">
</div>

Comportamiento en bash:

<div align="center">
    <img width="70%" src="../img/bash_2.png" alt="bash2">
</div>

---

### Tuberías múltiples
#### Investigar qué ocurre con el exit code reportado por la shell si se ejecuta un pipe
a. ¿Cambia en algo?  
b. ¿Qué ocurre si, en un pipe, alguno de los comandos falla? Mostrar evidencia (e.g. salidas de terminal) de este comportamiento usando bash. Comparar con su implementación.
- Al ejecutarse un pipe cada comando tiene su propio exit code, bash reporta unicamente el exit code del último comando del pipe, por medio de $?.
- Si alguno de los comandos falla, bash muestra por pantalla el mensaje del error. En nuestra complementación ocurre lo mismo. Ejemplos:

Los últimos dos comandos fallan y se muestra ambos errores en la salida:

<div align="center">
    <img width="70%" src="../img/1.png" alt="ejemplo1">
</div>

El último comando es correcto y se muestra su salida, además falla el intermedio y se muestra su error:

<div align="center">
    <img width="70%" src="../img/2.png" alt="ejemplo2">
</div>

Todos los comandos son válidos, pero únicamente se muestra la última salida:

<div align="center">
    <img width="70%" src="../img/3.png" alt="ejemplo2">
</div>

---

### Variables de entorno temporarias
#### 1. ¿Por qué es necesario hacerlo luego de la llamada a fork(2)?
- Las llamadas a setenv(3) modifican el entorno del proceso actual, dicho entorno no es compartido entre procesos. Si se realizan setenv en el proceso padre (antes de fork(2)), esas modificaciones persistirán en la shell y afectaran a todas las invocaciones posteriores, incumpliento con el caracter "temporal" de las asignaciones.  
Hacer las modificaciones en el hijo (después de fork(2) y antes de exec(3)) garantiza que sólo el proceso hijo recibe las variables temporales y el proceso padre conserva su entorno original.

#### 2. En algunos de los wrappers de la familia de funciones de exec(3) (las que finalizan con la letra e), se les puede pasar un tercer argumento (o una lista de argumentos dependiendo del caso), con nuevas variables de entorno para la ejecución de ese proceso. Supongamos, entonces, que en vez de utilizar setenv(3) por cada una de las variables, se guardan en un arreglo y se lo coloca en el tercer argumento de una de las funciones de exec(3).
a. ¿El comportamiento resultante es el mismo que en el primer caso? Explicar qué sucede y por qué.  
b. Describir brevemente (sin implementar) una posible implementación para que el comportamiento sea el mismo.
- No necesariamente el comportamiento es el mismo, las funciones finalizadas en 'e' reciben un arreglo con las variables lo que permite modificar el entorno heredado por defecto.
- Si se quisiera tener el mismo comportamiento es necesario que el arreglo incluya las variables originales del padre antes de añadir las temporales.
---

### Pseudo-variables
#### Investigar al menos otras tres variables mágicas estándar, y describir su propósito.
a. Incluir un ejemplo de su uso en bash (u otra terminal similar).
- **PID del proceso actual ($$):** Devuelve el ID del proceso de la shell en ejecución. Sirve para generar nombres únicos en archivos o rastrear procesos.

<div align="center">
    <img width="70%" src="../img/ejemplo1.png" alt="ej1">
</div>

- **PID del último proceso en segundo plano ($!):** Devuelve el ID del último proceso lanzado con &. Sirve para monitorear o terminar procesos en background.

<div align="center">
    <img width="70%" src="../img/ejemplo2.png" alt="ej2">
</div>

- **Útimo argumento del comando anterior ($_):** Almacena el último argumento del comando anterior, permite ejecutar comandos consecutivos.

<div align="center">
    <img width="70%" src="../img/ejemplo3.png" alt="ej3">
</div>

---

### Comandos built-in
#### ¿Entre cd y pwd, alguno de los dos se podría implementar sin necesidad de ser built-in? ¿Por qué? ¿Si la respuesta es sí, cuál es el motivo, entonces, de hacerlo como built-in? (para esta última pregunta pensar en los built-in como true y false)
- Si, pwd podría implementarse como un comando externo porque consulta y muestra el estado actual del directorio de trabajo sin alterar el comportamiento de la shell. Hacerlo built-in permite eficiencia y consistencia en la interpretación del directorio actual, evita la creación de un proceso hijo y depender de un binario externo.
---
### Procesos en segundo plano
#### Explicar detalladamente el mecanismo completo utilizado.
Al inicializar la shell con la función `init_shell()`, se llama a la función `sigaction_init()`.  
Aquí, se registra a `sigchld_handler()` como el handler de SIGCHLD, la señal que se recibe cuando un proceso hijo termina.
Es decir, cada vez un proceso hijo finalice, se ejecutará automáticamente esta función.  
El handler llama a `waitpid()` en bucle hasta que no encuentre más procesos del mismo grupo terminados, con el flag WNOHANG.
Este flag permite que `waitpid()` no se quede esperando a que termine un proceso hijo, evitando que se bloquee.  
Entonces, por cada proceso background que finaliza, se imprime su PID por pantalla inmediatamente.

#### ¿Por qué es necesario el uso de señales?
- La señal es una interrupción o notificación que permite manejar eventos asincrónicos. 
Para el caso de procesos en segundo plano, necesitamos una notificación inmediata de finalizacion, 
sin interferir con la ejecución de comandos en primer plano. La señal SIGCHLD es enviada por el sistema
cada vez que un proceso hijo termina, y el proceso padre ejecuta un handler que avisa al usuario que terminó un proceso.