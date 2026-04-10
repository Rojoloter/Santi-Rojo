#ifndef FS_H
#define FS_H

#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <stddef.h>

#define FS_MAX_INODES 256
#define FS_MAX_DATA 4096
#define FS_MAX_PATH 256

typedef enum { FS_FILE, FS_DIR } fs_type_t;

typedef struct {
	uid_t uid;
	gid_t gid;
	mode_t mode;
	nlink_t nlink;  // Contador de hard links

	time_t atime, mtime, ctime;
	size_t size;

	fs_type_t type;
	int used;
	char data[FS_MAX_DATA];
} fs_inode_t;

typedef struct {
	char name[FS_MAX_PATH];
	char path[FS_MAX_PATH];
	char parent[FS_MAX_PATH];

	int inode_index;
	int used;
} fs_dir_entry_t;

typedef struct {
	fs_inode_t inodes[FS_MAX_INODES];
	fs_dir_entry_t dir_entries[FS_MAX_INODES];
	size_t dir_count;
	size_t inode_count;
} fs_t;

extern fs_t fs;

void crear_directorio_raiz(fs_t *fs_ptr);

int indice_dir_entry(const char *path);

int crear_fs(const char *path, mode_t mode, fs_type_t type);

int guardar_fs(const char *filename);

int cargar_fs(const char *filename);

int separar_path(const char *path, char *parent, char *name);

#endif
