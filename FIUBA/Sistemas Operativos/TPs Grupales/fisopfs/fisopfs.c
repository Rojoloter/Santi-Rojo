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

#include "fs.h"

#define DEFAULT_FILE_DISK "persistence_file.fisopfs"
#define PATH_MAX 4096
#define MAX_DIR_DEPTH 3

static int
validate_path(const char *path)
{
	if (strlen(path) >= FS_MAX_PATH) {
		return -ENAMETOOLONG;
	}
	int depth = 0;
	for (const char *p = path; *p; p++) {
		if (*p == '/') {
			depth++;
		}
	}
	if (depth > MAX_DIR_DEPTH) {
		return -EPERM;
	}
	return 0;
}

static char filedisk_path[2 * PATH_MAX];

static fs_inode_t *
get_inode(int entry_idx)
{
	if (entry_idx < 0 || entry_idx >= FS_MAX_INODES)
		return NULL;
	int inode_idx = fs.dir_entries[entry_idx].inode_index;
	return &fs.inodes[inode_idx];
}

static void *
fisopfs_init(struct fuse_conn_info *conn)
{
	fprintf(stderr, "[debug] init\n");

	int r = cargar_fs(filedisk_path);
	if (r != 0) {
		fprintf(stderr,
		        "[debug] no existe '%s', creando FS nuevo\n",
		        filedisk_path);
		crear_directorio_raiz(&fs);
		guardar_fs(filedisk_path);
	}

	return NULL;
}

static void
fisopfs_destroy(void *data)
{
	fprintf(stderr, "[debug] destroy → guardar FS\n");
	guardar_fs(filedisk_path);
}


static int
fisopfs_flush(const char *path, struct fuse_file_info *fi)
{
	(void) path;
	(void) fi;
	fprintf(stderr, "[debug] flush\n");
	return guardar_fs(filedisk_path);
}


static int
fisopfs_getattr(const char *path, struct stat *st)
{
	printf("[debug] fisopfs_getattr - path: %s\n", path);
	memset(st, 0, sizeof(struct stat));

	int idx = indice_dir_entry(path);
	if (idx < 0) {
		return idx;
	}
	fs_inode_t *inode = get_inode(idx);
	st->st_ino = fs.dir_entries[idx].inode_index;
	st->st_uid = inode->uid;
	st->st_gid = inode->gid;
	st->st_size = inode->size;
	st->st_nlink = inode->nlink;
	st->st_atime = inode->atime;
	st->st_mtime = inode->mtime;
	st->st_ctime = inode->ctime;
	st->st_mode = inode->mode;

	return 0;
}

static int
fisopfs_readdir(const char *path,
                void *buffer,
                fuse_fill_dir_t filler,
                off_t offset,
                struct fuse_file_info *fi)
{
	(void) offset;
	(void) fi;

	printf("[debug] fisopfs_readdir - path: %s\n", path);

	int idx = indice_dir_entry(path);
	if (idx < 0) {
		return idx;
	}

	fs_inode_t *dir_inode = get_inode(idx);
	if (dir_inode->type != FS_DIR) {
		return -ENOTDIR;
	}

	filler(buffer, ".", NULL, 0);
	filler(buffer, "..", NULL, 0);

	for (int i = 0; i < FS_MAX_INODES; i++) {
		if (fs.dir_entries[i].used &&
		    strcmp(fs.dir_entries[i].parent, path) == 0) {
			filler(buffer, fs.dir_entries[i].name, NULL, 0);
		}
	}

	return 0;
}

static int
fisopfs_read(const char *path,
             char *buffer,
             size_t size,
             off_t offset,
             struct fuse_file_info *fi)
{
	(void) fi;
	printf("[debug] fisopfs_read - path: %s, offset: %lu, size: %lu\n",
	       path,
	       offset,
	       size);

	int idx = indice_dir_entry(path);
	if (idx < 0)
		return idx;

	fs_inode_t *inode = get_inode(idx);
	if (inode->type != FS_FILE)
		return -EISDIR;

	if ((size_t) offset >= inode->size) {
		return 0;
	}

	size_t available = inode->size - offset;
	size_t to_read = (size < available) ? size : available;

	memcpy(buffer, inode->data + offset, to_read);
	inode->atime = time(NULL);

	return (int) to_read;
}


static int
fisopfs_write(const char *path,
              const char *buffer,
              size_t size,
              off_t offset,
              struct fuse_file_info *fi)
{
	int idx = indice_dir_entry(path);
	if (idx < 0)
		return idx;

	fs_inode_t *inode = get_inode(idx);
	if (inode->type != FS_FILE)
		return -EISDIR;

	if ((size_t) offset > FS_MAX_DATA) {
		return -ENOSPC;
	}

	if ((size_t) offset > inode->size) {
		size_t gap = (size_t) offset - inode->size;
		if (inode->size + gap > FS_MAX_DATA) {
			return -ENOSPC;
		}
		memset(inode->data + inode->size, 0, gap);
		inode->size += gap;
	}

	if ((size_t) offset + size > FS_MAX_DATA) {
		return -ENOSPC;
	}

	memcpy(inode->data + offset, buffer, size);

	size_t new_end = (size_t) offset + size;
	if (new_end > inode->size) {
		inode->size = new_end;
	}

	time_t now = time(NULL);
	inode->mtime = now;
	inode->atime = now;

	return (int) size;
}

static int
fisopfs_truncate(const char *path, off_t size)
{
	if (size < 0 || size > FS_MAX_DATA) {
		return -EINVAL;
	}

	int idx = indice_dir_entry(path);
	if (idx < 0)
		return idx;

	fs_inode_t *inode = get_inode(idx);
	if (inode->type != FS_FILE)
		return -EISDIR;

	if ((size_t) size > inode->size) {
		memset(inode->data + inode->size, 0, (size_t) size - inode->size);
	} else {
		memset(inode->data + size, 0, inode->size - size);
	}
	inode->size = (size_t) size;
	inode->mtime = time(NULL);

	return 0;
}

static int
fisopfs_open(const char *path, struct fuse_file_info *fi)
{
	int idx = indice_dir_entry(path);
	return (idx < 0) ? idx : 0;
}

static int
fisopfs_create(const char *path, mode_t mode, struct fuse_file_info *fi)
{
	(void) fi;
	fprintf(stderr, "[debug] create - path: %s\n", path);
	if (validate_path(path) < 0)
		return -errno;
	return crear_fs(path, mode, FS_FILE);
}

static int
fisopfs_mkdir(const char *path, mode_t mode)
{
	fprintf(stderr, "[debug] mkdir - path: %s\n", path);
	if (validate_path(path) < 0)
		return -errno;
	return crear_fs(path, mode, FS_DIR);
}

static int
fisopfs_utimens(const char *path, const struct timespec tv[2])
{
	int idx = indice_dir_entry(path);
	if (idx < 0)
		return idx;

	fs_inode_t *inode = get_inode(idx);

	if (tv == NULL) {
		time_t now = time(NULL);
		inode->atime = now;
		inode->mtime = now;
	} else {
		inode->atime = tv[0].tv_sec;
		inode->mtime = tv[1].tv_sec;
	}

	return 0;
}

static int
fisopfs_link(const char *oldpath, const char *newpath)
{
	int old_idx = indice_dir_entry(oldpath);
	if (old_idx < 0)
		return old_idx;

	fs_inode_t *inode = get_inode(old_idx);
	if (inode->type == FS_DIR)
		return -EPERM;
	if (indice_dir_entry(newpath) >= 0)
		return -EEXIST;

	char parent_path[FS_MAX_PATH];
	char name[FS_MAX_PATH];
	int r = separar_path(newpath, parent_path, name);
	if (r < 0)
		return r;

	int parent_idx = indice_dir_entry(parent_path);
	if (parent_idx < 0)
		return parent_idx;

	fs_inode_t *parent_inode = get_inode(parent_idx);
	if (parent_inode->type != FS_DIR)
		return -ENOTDIR;

	int new_entry_idx = -1;
	for (int i = 0; i < FS_MAX_INODES; i++) {
		if (!fs.dir_entries[i].used) {
			new_entry_idx = i;
			break;
		}
	}
	if (new_entry_idx < 0)
		return -ENOSPC;

	if (validate_path(newpath) < 0)
		return -errno;

	fs_dir_entry_t *entry = &fs.dir_entries[new_entry_idx];
	strncpy(entry->name, name, FS_MAX_PATH - 1);
	entry->name[FS_MAX_PATH - 1] = '\0';
	strncpy(entry->path, newpath, FS_MAX_PATH - 1);
	entry->path[FS_MAX_PATH - 1] = '\0';
	strncpy(entry->parent, parent_path, FS_MAX_PATH - 1);
	entry->parent[FS_MAX_PATH - 1] = '\0';
	entry->inode_index = fs.dir_entries[old_idx].inode_index;
	entry->used = 1;
	inode->nlink++;
	inode->ctime = time(NULL);
	fs.dir_count++;
	guardar_fs(filedisk_path);
	return 0;
}

static int
fisopfs_unlink(const char *path)
{
	int idx = indice_dir_entry(path);
	if (idx < 0)
		return idx;

	fs_dir_entry_t *entry = &fs.dir_entries[idx];
	fs_inode_t *inode = get_inode(idx);
	if (inode->type != FS_FILE)
		return -EISDIR;

	entry->used = 0;
	fs.dir_count--;
	inode->nlink--;
	if (inode->nlink == 0) {
		memset(inode, 0, sizeof(*inode));
		fs.inode_count--;
	}
	guardar_fs(filedisk_path);

	return 0;
}

static int
fisopfs_rmdir(const char *path)
{
	fprintf(stderr, "[debug] rmdir - path: %s\n", path);

	int idx = indice_dir_entry(path);
	if (idx < 0)
		return idx;

	fs_inode_t *inode = get_inode(idx);
	if (inode->type != FS_DIR)
		return -ENOTDIR;

	if (strcmp(path, "/") == 0) {
		return -EPERM;
	}

	for (int i = 0; i < FS_MAX_INODES; i++) {
		if (fs.dir_entries[i].used &&
		    strcmp(fs.dir_entries[i].parent, path) == 0) {
			return -ENOTEMPTY;
		}
	}

	int parent_entry_idx = indice_dir_entry(fs.dir_entries[idx].parent);
	if (parent_entry_idx >= 0) {
		fs_inode_t *parent = get_inode(parent_entry_idx);
		if (parent->nlink > 0)
			parent->nlink--;
		parent->mtime = time(NULL);
	}
	memset(&fs.dir_entries[idx], 0, sizeof(fs_dir_entry_t));
	memset(inode, 0, sizeof(fs_inode_t));

	fs.inode_count--;
	fs.dir_count--;

	return 0;
}

static struct fuse_operations operations = {
	.init = fisopfs_init,
	.destroy = fisopfs_destroy,
	.flush = fisopfs_flush,
	.getattr = fisopfs_getattr,
	.readdir = fisopfs_readdir,
	.open = fisopfs_open,
	.create = fisopfs_create,
	.mkdir = fisopfs_mkdir,
	.read = fisopfs_read,
	.write = fisopfs_write,
	.truncate = fisopfs_truncate,
	.unlink = fisopfs_unlink,
	.rmdir = fisopfs_rmdir,
	.utimens = fisopfs_utimens,
	.link = fisopfs_link,
};


int
main(int argc, char *argv[])
{
	char *filedisk_name = (char *) DEFAULT_FILE_DISK;

	for (int i = 1; i < argc - 1; i++) {
		if (strcmp(argv[i], "--filedisk") == 0) {
			filedisk_name = argv[i + 1];

			for (int j = i; j < argc - 2; j++) {
				argv[j] = argv[j + 2];
			}
			argc -= 2;
			break;
		}
	}

	char cwd[PATH_MAX];
	if (!getcwd(cwd, sizeof(cwd))) {
		perror("getcwd");
		strncpy(filedisk_path, filedisk_name, sizeof(filedisk_path) - 1);
		filedisk_path[sizeof(filedisk_path) - 1] = '\0';
	} else {
		snprintf(filedisk_path,
		         sizeof(filedisk_path),
		         "%s/%s",
		         cwd,
		         filedisk_name);
	}

	fprintf(stderr, "[debug] usando archivo de disco: %s\n", filedisk_path);

	return fuse_main(argc, argv, &operations, NULL);
}
