#include "fs.h"

#define FUSE_USE_VERSION 30

#include <fuse.h>
#include <stdio.h>
#include <unistd.h>
#include <limits.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/file.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <time.h>

#define S_IFDIR 0040000
#define S_IFREG 0100000

fs_t fs;


static int
buscar_un_inodo_disponible(void)
{
	for (int i = 0; i < FS_MAX_INODES; i++) {
		if (!fs.inodes[i].used) {
			return i;
		}
	}
	return -1;
}

static int
buscar_dir_entry_disponible(void)
{
	for (int i = 0; i < FS_MAX_INODES; i++) {
		if (!fs.dir_entries[i].used) {
			return i;
		}
	}
	return -1;
}

static fs_dir_entry_t *
buscar_dir_entry_path(const char *path, int *idx_out)
{
	for (int i = 0; i < FS_MAX_INODES; i++) {
		if (fs.dir_entries[i].used &&
		    strcmp(fs.dir_entries[i].path, path) == 0) {
			if (idx_out)
				*idx_out = i;
			return &fs.dir_entries[i];
		}
	}
	return NULL;
}

void
crear_directorio_raiz(fs_t *fs_ptr)
{
	memset(fs_ptr, 0, sizeof(*fs_ptr));

	fs_inode_t *root_inode = &fs_ptr->inodes[0];
	root_inode->type = FS_DIR;
	root_inode->size = 0;
	memset(root_inode->data, 0, FS_MAX_DATA);
	root_inode->uid = getuid();
	root_inode->gid = getgid();
	root_inode->mode = S_IFDIR | 0755;
	root_inode->nlink = 2;  // . y ..
	time_t now = time(NULL);
	root_inode->atime = root_inode->mtime = root_inode->ctime = now;
	root_inode->used = 1;

	fs_dir_entry_t *root_entry = &fs_ptr->dir_entries[0];
	strcpy(root_entry->name, "/");
	strcpy(root_entry->path, "/");
	strcpy(root_entry->parent, "");
	root_entry->inode_index = 0;
	root_entry->used = 1;

	fs_ptr->inode_count = 1;
	fs_ptr->dir_count = 1;
}


int
indice_dir_entry(const char *path)
{
	int idx;
	if (!buscar_dir_entry_path(path, &idx)) {
		return -ENOENT;
	}
	return idx;
}

int
separar_path(const char *path, char *parent, char *name)
{
	if (path[0] != '/') {
		return -EINVAL;
	}
	if (strlen(path) >= FS_MAX_PATH) {
		return -ENAMETOOLONG;
	}

	const char *slash = strrchr(path, '/');

	if (!slash) {
		return -EINVAL;
	}

	if (slash == path) {
		strcpy(parent, "/");
		strncpy(name, slash + 1, FS_MAX_PATH - 1);
		name[FS_MAX_PATH - 1] = '\0';
	} else {
		size_t plen = (size_t) (slash - path);
		if (plen >= FS_MAX_PATH)
			return -ENAMETOOLONG;

		memcpy(parent, path, plen);
		parent[plen] = '\0';

		strncpy(name, slash + 1, FS_MAX_PATH - 1);
		name[FS_MAX_PATH - 1] = '\0';
	}

	return 0;
}

int
crear_fs(const char *path, mode_t mode, fs_type_t type)
{
	if (strcmp(path, "/") == 0) {
		return -EEXIST;
	}

	if (buscar_dir_entry_path(path, NULL)) {
		return -EEXIST;
	}

	char parent_path[FS_MAX_PATH];
	char name[FS_MAX_PATH];

	int r = separar_path(path, parent_path, name);
	if (r < 0) {
		return r;
	}

	int parent_entry_idx = indice_dir_entry(parent_path);
	if (parent_entry_idx < 0) {
		return parent_entry_idx;
	}

	int parent_inode_idx = fs.dir_entries[parent_entry_idx].inode_index;
	fs_inode_t *parent_inode = &fs.inodes[parent_inode_idx];
	if (parent_inode->type != FS_DIR) {
		return -ENOTDIR;
	}

	int inode_idx = buscar_un_inodo_disponible();
	int entry_idx = buscar_dir_entry_disponible();
	if (inode_idx < 0 || entry_idx < 0) {
		return -ENOSPC;
	}

	fs_inode_t *inode = &fs.inodes[inode_idx];
	memset(inode, 0, sizeof(*inode));
	inode->type = type;
	inode->size = 0;
	memset(inode->data, 0, FS_MAX_DATA);
	inode->uid = getuid();
	inode->gid = getgid();
	mode_t perm = mode & 0777;
	if (type == FS_FILE) {
		inode->mode = S_IFREG | perm;
		inode->nlink = 1;
	} else {
		inode->mode = S_IFDIR | perm;
		inode->nlink = 2;
	}

	time_t now = time(NULL);
	inode->atime = inode->mtime = inode->ctime = now;
	inode->used = 1;

	fs_dir_entry_t *entry = &fs.dir_entries[entry_idx];
	strncpy(entry->name, name, FS_MAX_PATH);
	strncpy(entry->path, path, FS_MAX_PATH);
	strncpy(entry->parent, parent_path, FS_MAX_PATH);
	entry->name[FS_MAX_PATH - 1] = '\0';
	entry->path[FS_MAX_PATH - 1] = '\0';
	entry->parent[FS_MAX_PATH - 1] = '\0';
	entry->inode_index = inode_idx;
	entry->used = 1;

	fs.inode_count++;
	fs.dir_count++;

	if (type == FS_DIR) {
		parent_inode->nlink++;
	}
	parent_inode->mtime = now;

	return 0;
}

int
guardar_fs(const char *filename)
{
	FILE *f = fopen(filename, "wb");
	if (!f) {
		perror("fs_serialize fopen");
		return -EIO;
	}

	size_t n = fwrite(&fs, sizeof(fs), 1, f);
	if (n != 1) {
		perror("fs_serialize fwrite");
		fclose(f);
		return -EIO;
	}

	fclose(f);
	return 0;
}

int
cargar_fs(const char *filename)
{
	FILE *f = fopen(filename, "rb");
	if (!f) {
		return -ENOENT;
	}

	size_t n = fread(&fs, sizeof(fs), 1, f);
	if (n != 1) {
		perror("fs_deserialize fread");
		fclose(f);
		return -EIO;
	}

	fclose(f);
	return 0;
}