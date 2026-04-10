# fisop-fs

## Estructuras en memoria para almacenar archivos, directorios y metadatos

### `struct fs_t`
El sistema de archivos se organiza alrededor de una estructura principal llamada `fs_t`. Esta estructura contiene toda la información del sistema de archivos y reside en memoria durante la ejecución:

* **`inodes`**: Un array estático de estructuras `fs_inode_t` con un tamaño fijo definido por `FS_MAX_INODES` (256).
* **`inodes_count`**: Un contador de tipo `size_t` que lleva el registro de la cantidad actual de inodos.

### `struct fs_inode_t` (Inodos)
`fs_inode_t` contiene tanto los metadatos como los datos del archivo. Cada elemento del arreglo `inodes` incluye:

**Identificación:**
* **`path`**: Almacena la ruta absoluta completa del archivo o directorio.
* **`name`**: Nombre relativo del archivo/directorio.
* **`parent`**: Ruta absoluta del directorio padre.

**Metadatos:**
* **`type`**: Enum `fs_type_t` que distingue entre `FS_FILE` (archivo) y `FS_DIR` (directorio).
* **`uid`, `gid`**: Identificadores de usuario y grupo.
* **`mode`**: Permisos y modo del archivo.
* **`atime`, `mtime`, `ctime`**: Tiempo de acceso, modificación y creación.
* **`used`**: Flag que indica si el inodo está asignado o libre.

**Datos:**
* **`data`**: Un arreglo de caracteres de tamaño fijo (`FS_MAX_DATA`, 4096) donde se almacena el contenido del archivo.
* **`size`**: Tamaño actual de los datos almacenados.

### Bloque Raíz
El directorio raíz (`/`) se inicializa en la función `crear_directorio_raiz`, ocupando el índice 0 del arreglo de inodos, con tipo `FS_DIR`, y `parent` vacío.

## Cómo el sistema de archivos encuentra un archivo específico dado un path

### Mecanismo de Búsqueda (`indice_inodo` y `buscar_inodo_path`)
Para encontrar un archivo específico:

1.  Se invoca la función `indice_inodo` con el path completo deseado.
2.  Esta llama a `buscar_inodo_path`, la cual recorre iterativamente el arreglo `fs.inodes` desde el índice 0 hasta `FS_MAX_INODES`.
3.  En cada iteración, verifica dos condiciones:
    * Que el inodo esté en uso (`used == 1`).
    * Que el campo `path` del inodo coincida con la ruta buscada usando `strcmp`.

Si encuentra coincidencia, `indice_inodo` retorna el índice al inodo, de lo contrario devuelve error (`-ENOENT`).

### Listado de Directorios (`fisopfs_readdir`)
Para listar el contenido de un directorio, el sistema recorre nuevamente todo el arreglo de inodos y filtra aquellos cuyo campo `parent` coincida con el path del directorio consultado.

## Estructuras auxiliares utilizadas

`fs.h` y `fs.c` definen constantes y funciones auxiliares:

**Constantes**
* `FS_MAX_INODES` (256): Límite estricto de la cantidad de archivos y directorios que el sistema puede alojar.
* `FS_MAX_DATA` (4096): Tamaño máximo en bytes para el contenido de un archivo individual.
* `FS_MAX_PATH` (256): Longitud máxima permitida para las rutas y nombres de archivo.

**Enums**
* `fs_type_t`: Enumera los tipos de nodos soportados, `FS_FILE` (archivo regular) y `FS_DIR` (directorio).

**Funciones auxiliares**
* `separar_path`: Una función auxiliar que divide una ruta completa en dos componentes: el directorio padre (`parent`) y el nombre del archivo (`name`).

## El formato de serialización del sistema de archivos en disco

### Mecanismo de Guardado (`guardar_fs`)
El sistema implementa la persistencia copiando el estado completo de la memoria hacia el disco rígido. En lugar de procesar cada archivo por separado, se realiza una copia directa de toda la estructura de datos.

* **Proceso de escritura:** Se utiliza la función `fwrite` para tomar la estructura principal `fs` (que contiene todos los archivos, carpetas y datos actuales) y guardarla en el disco.
* **Archivo de destino:** Esta copia se almacena por defecto en el archivo `persistence_file.fisopfs`, salvo que el usuario especifique una ruta personalizada al iniciar el programa.

### Mecanismo de Carga (`cargar_fs`)
Al iniciar (`fisopfs_init`), el sistema intenta leer el archivo de disco utilizando `fread` directamente sobre la variable global `fs`. Si el archivo existe y la lectura es exitosa, el estado de la memoria se restaura exactamente como estaba al momento del último guardado. Si no existe, se formatea un nuevo sistema de archivos en memoria.

---

## Test

Para ejecutar los tests:
```bash
make test
```

### Salida esperada:

```bash
=== Compilando la solución ===
gcc -ggdb3 -O2 -Wall -std=c11 -Wno-unused-function -Wvla -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -D_FILE_OFFSET_BITS=64  -c fisopfs.c -o fisopfs.o
gcc -ggdb3 -O2 -Wall -std=c11 -Wno-unused-function -Wvla -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -D_FILE_OFFSET_BITS=64  -c fs.c -o fs.o
gcc -ggdb3 -O2 -Wall -std=c11 -Wno-unused-function -Wvla -D_FILE_OFFSET_BITS=64 -I/usr/include/fuse -D_FILE_OFFSET_BITS=64  -o fisopfs fisopfs.o fs.o -lfuse -pthread 
=== Creando la carpeta para montar el sistema de archivos ===
=== Desmontando si ya existe un montaje previo ===
umount: prueba: no montado.
=== Montando el sistema de archivos ===
[debug] usando archivo de disco: /home/mml/fiuba/sisop/sisop_2025b_g57/fisopfs/persistence_file.fisopfs

=== Test básicos ===

=== Crear directorio en root vacío ===
✔ Directorio se crea exitosamente.
=== Prueba de eliminación de directorio en root ===
✔ Directorio se elimina exitosamente.
=== Prueba de creación de archivo en root ===
✔ Archivo se crea exitosamente.
=== Prueba de escritura en archivo en root ===
✔ Escritura en archivo exitosa.
=== Prueba de eliminación de archivo en root ===
✔ Archivo se elimina exitosamente.
=== Prueba de creación de directorio en directorio ===
✔ Directorio se crea exitosamente.
=== Prueba de eliminación de directorio en directorio ===
✔ Directorio se elimina exitosamente.
=== Prueba de creación de archivo en directorio ===
✔ Archivo se crea exitosamente.
=== Prueba de eliminación de archivo en directorio ===
✔ Archivo se elimina exitosamente.

=== Tests de lectura y escritura ===

=== Prueba de append (>>) en archivo ===
✔ Append en archivo exitoso.
=== Prueba de lectura con cat ===
✔ Lectura con cat exitosa.
=== Prueba de truncamiento con > ===
✔ Truncamiento con > exitoso.

=== Tests de directorios ===

=== Prueba de ls en directorio ===
✔ ls muestra archivos correctamente.
=== Prueba de . y .. en directorios ===
✔ Pseudo-directorios . y .. presentes.
=== Prueba de rmdir en directorio vacío ===
✔ rmdir elimina directorio vacío exitosamente.
=== Prueba de rmdir en directorio no vacío ===
rmdir: fallo al borrar 'prueba/dir_no_vacio': El directorio no está vacío
✔ rmdir rechaza correctamente directorio no vacío.

=== Desmontando el sistema de archivos ===
```