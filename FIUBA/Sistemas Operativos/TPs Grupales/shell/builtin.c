#include "builtin.h"

//  returns true if the 'exit' call
//  should be performed
//
//  (It must not be called from here)
int
exit_shell(char *cmd)
{
	if (strcmp(cmd, "exit") == 0) {
		exit(0);
	}

	return 0;
}

void
actualizar_prompt()
{
	char *cwd = getcwd(NULL, 0);
	if (cwd != NULL) {
		snprintf(prompt, sizeof prompt, "(%s)", cwd);
	} else {
		perror("pwd");
	}
	free(cwd);
}

// returns true if "chdir" was performed
//  this means that if 'cmd' contains:
// 	1. $ cd directory (change to 'directory')
// 	2. $ cd (change to $HOME)
//  it has to be executed and then return true
//
//  Remember to update the 'prompt' with the
//  	new directory.
//
// Examples:
//  1. cmd = ['c','d', ' ', '/', 'b', 'i', 'n', '\0']
//  2. cmd = ['c','d', '\0']
int
cd(char *cmd)
{
	if (strncmp(cmd, "cd", 2) == 0 && (cmd[2] == ' ' || cmd[2] == '\0')) {
		char *path = cmd + 2;
		while (*path == ' ') {
			path++;
		}
		if (*path == '\0') {
			path = getenv("HOME");
			if (!path) {
				fprintf(stderr, "cd: HOME nt set\n");

				return 1;
			}
		}
		if (chdir(path) != 0) {
			switch (errno) {
			case ENOENT:
				fprintf(stderr, "cannot cd to %s : No such file or directory\n", path);
				break;
			case EACCES:
				fprintf(stderr,
				        "cannot cd to %s : Permission denied\n",
				        path);
				break;
			case ENOTDIR:
				fprintf(stderr,
				        "cannot cd to %s : Not a directory\n",
				        path);
				break;
			default:
				fprintf(stderr,
				        "cannot cd to %s : %s\n",
				        path,
				        strerror(errno));
				break;
			}
		}
		actualizar_prompt();

		return 1;
	}
	return 0;
}

// returns true if 'pwd' was invoked
// in the command line
//
// (It has to be executed here and then
// 	return true)
int
pwd(char *cmd)
{
	if (strncmp(cmd, "pwd", 3) == 0) {
		char cwd[BUFLEN];
		if (getcwd(cwd, sizeof(cwd)) != NULL) {
			printf("%s\n", cwd);
		} else {
			perror("pwd");
		}
		return 1;
	}

	return 0;
}

// returns true if `history` was invoked
// in the command line
//
// (It has to be executed here and then
// 	return true)
int
history(char *cmd)
{
	// Your code here

	return 0;
}
