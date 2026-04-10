#!/bin/bash

# ====== Colores ======
GREEN='\033[0;32m'
BLUE='\033[94m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

TICK="${GREEN}✔${NC}"
CROSS="${RED}✘${NC}"

MOUNT_POINT="prueba"
FUSE_PROGRAM="./fisopfs -o use_ino -o entry_timeout=0 -o attr_timeout=0 -o negative_timeout=0"

print_msg() {
    local symbol=$1
    local message=$2
    echo -e "${symbol} ${message}"
}

sanear_directorios() {
    find "$MOUNT_POINT" -mindepth 1 -delete
}

echo -e "${YELLOW}=== Compilando la solución ===${NC}"
make || { echo -e "${RED}Error en compilación${NC}"; exit 1; }

echo -e "${YELLOW}=== Creando la carpeta para montar el sistema de archivos ===${NC}"
mkdir -p "$MOUNT_POINT"

echo -e "${YELLOW}=== Desmontando si ya existe un montaje previo ===${NC}"
sudo umount "$MOUNT_POINT"

echo -e "${YELLOW}=== Montando el sistema de archivos ===${NC}"
$FUSE_PROGRAM "$MOUNT_POINT"

test_crear_dir_en_root() {
    echo "=== Crear directorio en root vacío ==="
    sanear_directorios
    local route="$MOUNT_POINT/directorio_prueba"
    
    if mkdir "$route"  && [[ -d "$route" ]]; then
        print_msg "$TICK" "Directorio se crea exitosamente."
        return 0
    else
        print_msg "$CROSS" "No se encuentra el directorio en root."
        return 1
    fi
}

test_eliminar_dir_en_root() {
    echo "=== Prueba de eliminación de directorio en root ==="
    sanear_directorios
    local route="$MOUNT_POINT/directorio_prueba"
    
    mkdir "$route"  || { print_msg "$CROSS" "No se pudo crear directorio"; return 1; }
    
    if rmdir "$route"  && [[ ! -d "$route" ]]; then
        print_msg "$TICK" "Directorio se elimina exitosamente."
        return 0
    else
        print_msg "$CROSS" "No se eliminó el directorio."
        return 1
    fi
}

test_crear_archivo_en_root() {
    echo "=== Prueba de creación de archivo en root ==="
    sanear_directorios
    local route="$MOUNT_POINT/archivo_prueba.txt"
    
    if touch "$route"  && [[ -f "$route" ]]; then
        print_msg "$TICK" "Archivo se crea exitosamente."
        return 0
    else
        print_msg "$CROSS" "No se encuentra el archivo en root."
        return 1
    fi
}

test_escribir_archivo_en_root() {
    echo "=== Prueba de escritura en archivo en root ==="
    sanear_directorios
    local route="$MOUNT_POINT/archivo_prueba.txt"
    local string="Probando file system"
    
    echo "$string" > "$route"  || { print_msg "$CROSS" "No se pudo escribir"; return 1; }
    local buffer=$(cat "$route" )
    
    if [[ "$buffer" == "$string" ]]; then
        print_msg "$TICK" "Escritura en archivo exitosa."
        return 0
    else
        print_msg "$CROSS" "Escritura en archivo fallida."
        return 1
    fi
}

test_eliminar_archivo_en_root() {
    echo "=== Prueba de eliminación de archivo en root ==="
    sanear_directorios
    local route="$MOUNT_POINT/archivo_prueba.txt"
    
    touch "$route"  || { print_msg "$CROSS" "No se pudo crear archivo"; return 1; }
    
    if rm "$route"  && [[ ! -f "$route" ]]; then
        print_msg "$TICK" "Archivo se elimina exitosamente."
        return 0
    else
        print_msg "$CROSS" "No se eliminó el archivo."
        return 1
    fi
}

test_crear_dir_en_dir() {
    echo "=== Prueba de creación de directorio en directorio ==="
    sanear_directorios
    
    mkdir "$MOUNT_POINT/directorio_prueba"  || { print_msg "$CROSS" "No se pudo crear directorio padre"; return 1; }
    mkdir "$MOUNT_POINT/directorio_prueba/directorio_prueba2"  || { print_msg "$CROSS" "No se pudo crear directorio hijo"; return 1; }
    
    if [[ -d "$MOUNT_POINT/directorio_prueba/directorio_prueba2" ]]; then
        print_msg "$TICK" "Directorio se crea exitosamente."
        return 0
    else
        print_msg "$CROSS" "No se encuentra el directorio en el directorio padre."
        return 1
    fi
}

test_eliminar_dir_en_dir() {
    echo "=== Prueba de eliminación de directorio en directorio ==="
    sanear_directorios
    
    mkdir -p "$MOUNT_POINT/directorio_prueba/directorio_prueba2"  || { print_msg "$CROSS" "No se pudieron crear directorios"; return 1; }
    
    if rmdir "$MOUNT_POINT/directorio_prueba/directorio_prueba2"  && [[ ! -d "$MOUNT_POINT/directorio_prueba/directorio_prueba2" ]]; then
        print_msg "$TICK" "Directorio se elimina exitosamente."
        return 0
    else
        print_msg "$CROSS" "No se eliminó el directorio."
        return 1
    fi
}

test_crear_archivo_en_dir() {
    echo "=== Prueba de creación de archivo en directorio ==="
    sanear_directorios
    
    mkdir "$MOUNT_POINT/directorio_prueba"  || { print_msg "$CROSS" "No se pudo crear directorio"; return 1; }
    touch "$MOUNT_POINT/directorio_prueba/archivo_prueba.txt"  || { print_msg "$CROSS" "No se pudo crear archivo"; return 1; }
    
    if [[ -f "$MOUNT_POINT/directorio_prueba/archivo_prueba.txt" ]]; then
        print_msg "$TICK" "Archivo se crea exitosamente."
        return 0
    else
        print_msg "$CROSS" "No se encuentra el archivo en el directorio."
        return 1
    fi
}

test_eliminar_archivo_en_dir() {
    echo "=== Prueba de eliminación de archivo en directorio ==="
    sanear_directorios
    
    mkdir "$MOUNT_POINT/directorio_prueba"  || { print_msg "$CROSS" "No se pudo crear directorio"; return 1; }
    touch "$MOUNT_POINT/directorio_prueba/archivo_prueba.txt"  || { print_msg "$CROSS" "No se pudo crear archivo"; return 1; }
    
    if rm "$MOUNT_POINT/directorio_prueba/archivo_prueba.txt"  && [[ ! -f "$MOUNT_POINT/directorio_prueba/archivo_prueba.txt" ]]; then
        print_msg "$TICK" "Archivo se elimina exitosamente."
        return 0
    else
        print_msg "$CROSS" "No se eliminó el archivo."
        return 1
    fi
}

test_append_archivo() {
    echo "=== Prueba de append (>>) en archivo ==="
    sanear_directorios
    local route="$MOUNT_POINT/archivo_prueba.txt"
    local string1="Primera linea"
    local string2="Segunda linea"
    
    echo "$string1" > "$route"  || { print_msg "$CROSS" "No se pudo escribir"; return 1; }
    echo "$string2" >> "$route"  || { print_msg "$CROSS" "No se pudo hacer append"; return 1; }
    local buffer=$(cat "$route" )
    local expected="$string1
$string2"
    
    if [[ "$buffer" == "$expected" ]]; then
        print_msg "$TICK" "Append en archivo exitoso."
        return 0
    else
        print_msg "$CROSS" "Append en archivo fallido."
        return 1
    fi
}

test_leer_archivo_con_cat() {
    echo "=== Prueba de lectura con cat ==="
    sanear_directorios
    local route="$MOUNT_POINT/archivo_prueba.txt"
    local string="Contenido para leer con cat"
    
    echo "$string" > "$route"  || { print_msg "$CROSS" "No se pudo escribir"; return 1; }
    local buffer=$(cat "$route" )
    
    if [[ "$buffer" == "$string" ]]; then
        print_msg "$TICK" "Lectura con cat exitosa."
        return 0
    else
        print_msg "$CROSS" "Lectura con cat fallida."
        return 1
    fi
}

test_truncamiento_escritura() {
    echo "=== Prueba de truncamiento con > ==="
    sanear_directorios
    local route="$MOUNT_POINT/archivo_trunc.txt"
    
    echo "contenido largo original" > "$route"  || { print_msg "$CROSS" "No se pudo escribir"; return 1; }
    echo "corto" > "$route"  || { print_msg "$CROSS" "No se pudo truncar"; return 1; }
    local buffer=$(cat "$route" )
    
    if [[ "$buffer" == "corto" ]]; then
        print_msg "$TICK" "Truncamiento con > exitoso."
        return 0
    else
        print_msg "$CROSS" "Truncamiento con > fallido."
        return 1
    fi
}

test_ls_directorio() {
    echo "=== Prueba de ls en directorio ==="
    sanear_directorios
    
    mkdir "$MOUNT_POINT/dir_test"  || { print_msg "$CROSS" "No se pudo crear directorio"; return 1; }
    touch "$MOUNT_POINT/dir_test/archivo1.txt" 
    touch "$MOUNT_POINT/dir_test/archivo2.txt" 
    
    local output=$(ls "$MOUNT_POINT/dir_test" )
    
    if [[ "$output" == *"archivo1.txt"* ]] && [[ "$output" == *"archivo2.txt"* ]]; then
        print_msg "$TICK" "ls muestra archivos correctamente."
        return 0
    else
        print_msg "$CROSS" "ls no muestra archivos correctamente."
        return 1
    fi
}

test_punto_y_doble_punto() {
    echo "=== Prueba de . y .. en directorios ==="
    sanear_directorios
    
    mkdir -p "$MOUNT_POINT/dir1/dir2"  || { print_msg "$CROSS" "No se pudieron crear directorios"; return 1; }
    
    local output=$(ls -a "$MOUNT_POINT/dir1" )
    
    if [[ "$output" == *"."* ]] && [[ "$output" == *".."* ]]; then
        print_msg "$TICK" "Pseudo-directorios . y .. presentes."
        return 0
    else
        print_msg "$CROSS" "Pseudo-directorios . y .. ausentes."
        return 1
    fi
}

test_rmdir_directorio_no_vacio() {
    echo "=== Prueba de rmdir en directorio no vacío ==="
    sanear_directorios
    
    mkdir "$MOUNT_POINT/dir_no_vacio"  || { print_msg "$CROSS" "No se pudo crear directorio"; return 1; }
    touch "$MOUNT_POINT/dir_no_vacio/archivo.txt" 
    
    if rmdir "$MOUNT_POINT/dir_no_vacio" ; then
        print_msg "$CROSS" "rmdir eliminó directorio no vacío (comportamiento incorrecto)."
        return 1
    else
        print_msg "$TICK" "rmdir rechaza correctamente directorio no vacío."
        return 0
    fi
}

test_crear_hard_link() {
    echo "=== Prueba de creación de hard link ==="
    sanear_directorios
    local target="$MOUNT_POINT/archivo_target.txt"
    local link="$MOUNT_POINT/archivo_link.txt"

    touch "$target"

    if ln "$target" "$link"; then
        if [[ -f "$link" ]]; then
             local nlink=$(stat -c %h "$target")
             if [[ "$nlink" -eq 2 ]]; then
                 print_msg "$TICK" "Hard link creado y contador correcto (2)."
                 return 0
             else
                 print_msg "$CROSS" "Hard link creado pero contador incorrecto: $nlink."
                 return 1
             fi
        else
             print_msg "$CROSS" "El comando ln tuvo éxito pero el archivo no existe."
             return 1
        fi
    else
        print_msg "$CROSS" "Fallo al ejecutar ln."
        return 1
    fi
}

test_hard_link_datos_compartidos() {
    echo "=== Prueba de consistencia de datos en hard links ==="
    sanear_directorios
    local target="$MOUNT_POINT/archivo_A.txt"
    local link="$MOUNT_POINT/archivo_B.txt"
    local texto="Texto compartido"

    touch "$target"
    ln "$target" "$link"

    echo "$texto" > "$link"
    local contenido=$(cat "$target")

    if [[ "$contenido" == "$texto" ]]; then
        print_msg "$TICK" "Modificación en link se refleja en el original."
        return 0
    else
        print_msg "$CROSS" "Los datos no se compartieron correctamente."
        return 1
    fi
}

test_hard_link_unlink() {
    echo "=== Prueba de persistencia tras eliminar origen (unlink) ==="
    sanear_directorios
    local target="$MOUNT_POINT/archivo_base.txt"
    local link="$MOUNT_POINT/archivo_copia.txt"

    echo "Dato" > "$target"
    ln "$target" "$link"
    rm "$target"
    if [[ -f "$link" ]]; then
        local contenido=$(cat "$link")
        if [[ "$contenido" == "Dato" ]]; then
            print_msg "$TICK" "El archivo persiste a través del link."
            local nlink=$(stat -c %h "$link")
            if [[ "$nlink" -eq 1 ]]; then
                 print_msg "$TICK" "Contador de links se actualizó a 1."
                 return 0
            else
                 print_msg "$CROSS" "Contador de links no bajó a 1 (valor: $nlink)."
                 return 1
            fi
        else
            print_msg "$CROSS" "El contenido se perdió o corrompió."
            return 1
        fi
    else
        print_msg "$CROSS" "El link se borró accidentalmente."
        return 1
    fi
}

test_hard_link_a_directorio() {
    echo "=== Prueba de prohibición de hard link a directorio ==="
    sanear_directorios
    mkdir "$MOUNT_POINT/dir_prueba"
    if ln "$MOUNT_POINT/dir_prueba" "$MOUNT_POINT/link_dir" 2>/dev/null; then
        print_msg "$CROSS" "Se permitió crear hard link a directorio (ERROR)."
        return 1
    else
        print_msg "$TICK" "El sistema rechazó crear hard link a directorio."
        return 0
    fi
}

test_path_longitud_excesiva() {
    echo "=== Prueba de Longitud de Path Excesiva (>256) ==="
    sanear_directorios
    local nombre_largo="/$(printf 'a%.0s' {1..260})"

    if touch "$MOUNT_POINT$nombre_largo" 2>/dev/null; then
        print_msg "$CROSS" "El sistema permitió un path mayor a FS_MAX_PATH (ERROR)."
        return 1
    else
        print_msg "$TICK" "El sistema bloqueó correctamente el path excesivamente largo."
        return 0
    fi
}

test_anidamiento_niveles_permitidos() {
    echo "=== Prueba de Anidamiento: Niveles permitidos (1-3) ==="
    sanear_directorios

    if ! mkdir "$MOUNT_POINT/dir1"; then
        print_msg "$CROSS" "Fallo creando nivel 1."
        return 1
    fi

    if ! mkdir "$MOUNT_POINT/dir1/dir2"; then
        print_msg "$CROSS" "Fallo creando nivel 2."
        return 1
    fi

    if mkdir "$MOUNT_POINT/dir1/dir2/dir3"; then
        print_msg "$TICK" "Se permitió crear hasta el nivel máximo (3) correctamente."
        return 0
    else
        print_msg "$CROSS" "Fallo creando el nivel límite (3)."
        return 1
    fi
}

test_anidamiento_mkdir_excesivo() {
    echo "=== Prueba de Anidamiento: Bloqueo de mkdir excesivo (Nivel 4) ==="
    mkdir -p "$MOUNT_POINT/dir1/dir2/dir3" 2>/dev/null

    if mkdir "$MOUNT_POINT/dir1/dir2/dir3/dir4" 2>/dev/null; then
        print_msg "$CROSS" "Se permitió crear directorio en nivel 4 (ERROR)."
        return 1
    else
        print_msg "$TICK" "El sistema bloqueó correctamente mkdir en profundidad excesiva."
        return 0
    fi
}

test_anidamiento_archivo_excesivo() {
    echo "=== Prueba de Anidamiento: Bloqueo de archivo excesivo (Nivel 4) ==="
    local archivo_profundo="$MOUNT_POINT/dir1/dir2/dir3/archivo_profundo.txt"

    if touch "$archivo_profundo" 2>/dev/null; then
        print_msg "$CROSS" "Se permitió crear archivo en nivel 4 (ERROR)."
        return 1
    else
        print_msg "$TICK" "El sistema bloqueó correctamente touch en profundidad excesiva."
        return 0
    fi
}

echo -e "${BLUE}\n=== Test básicos ===${NC}\n"
test_crear_dir_en_root
test_eliminar_dir_en_root
test_crear_archivo_en_root
test_escribir_archivo_en_root
test_eliminar_archivo_en_root
test_crear_dir_en_dir
test_eliminar_dir_en_dir
test_crear_archivo_en_dir
test_eliminar_archivo_en_dir

echo -e "${BLUE}\n=== Tests de lectura y escritura ===${NC}\n"
test_append_archivo
test_leer_archivo_con_cat
test_truncamiento_escritura

echo -e "${BLUE}\n=== Tests de directorios ===${NC}\n"
test_ls_directorio
test_punto_y_doble_punto
test_rmdir_directorio_no_vacio

echo -e "${BLUE}\n=== Tests de Hard Links ===${NC}\n"
test_crear_hard_link
test_hard_link_datos_compartidos
test_hard_link_unlink
test_hard_link_a_directorio

echo -e "${BLUE}\n=== Tests de Multiples Directorios Anidados ===${NC}\n"
test_anidamiento_niveles_permitidos
test_anidamiento_mkdir_excesivo
test_anidamiento_archivo_excesivo
test_path_longitud_excesiva

echo -e "${YELLOW}\n=== Desmontando el sistema de archivos ===${NC}"
sudo umount -l "$MOUNT_POINT"