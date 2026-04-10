#include "exec.h"

#define SETENV_ERROR "Error setenv, no se pudo setear la clave y valor"
#define BACK_CMD_ERROR "Error backcdm"
#define EXECVP_ERROR "Error execvp"
#define ARCHIVO_INVALIDO_ERROR "Error archivo invalido"
#define ARCHIVO_ERROR "Error lectura de archivo"
#define DUP_ERROR "Error dup de archivo"
#define PIPE_ERROR "Error crear pipe"
#define FORK_ERROR "Error fork"
#define LEFT_ERROR "Error left"
#define RIGTH_ERROR "Error rigth"
#define WPID_ERROR "Wait_paid_error fallo"
#define FAIL_ERROR -1

static int open_redir_fd(char *file, int flags);
static void manejo_de_archivos(char *archivo, int flags, int lectura);
static void
manejo_de_archivos(char *archivo, int flags, int lectura)
{
	if (!archivo || archivo[0] == '\0') {
		perror(ARCHIVO_INVALIDO_ERROR);
		_exit(-1);
	}
	if (strlen(archivo) > 0) {
		int file_descriptor = open_redir_fd(archivo, flags);
		if (file_descriptor < 0) {
			perror(ARCHIVO_ERROR);
			exit(-1);
		}
		if (dup2(file_descriptor, lectura) < 0) {
			perror(DUP_ERROR);
		}
		close(file_descriptor);
	}
}
// sets "key" with the key part of "arg"
// and null-terminates it
//
// Example:
//  - KEY=value
//  arg = ['K', 'E', 'Y', '=', 'v', 'a', 'l', 'u', 'e', '\0']
//  key = "KEY"
//
static void
get_environ_key(char *arg, char *key)
{
	int i;
	for (i = 0; arg[i] != '='; i++)
		key[i] = arg[i];

	key[i] = END_STRING;
}

// sets "value" with the value part of "arg"
// and null-terminates it
// "idx" should be the index in "arg" where "=" char
// resides
//
// Example:
//  - KEY=value
//  arg = ['K', 'E', 'Y', '=', 'v', 'a', 'l', 'u', 'e', '\0']
//  value = "value"
//
static void
get_environ_value(char *arg, char *value, int idx)
{
	size_t i, j;
	for (i = (idx + 1), j = 0; i < strlen(arg); i++, j++)
		value[j] = arg[i];

	value[j] = END_STRING;
}

// sets the environment variables received
// in the command line
//
// Hints:
// - use 'block_contains()' to
// 	get the index where the '=' is
// - 'get_environ_*()' can be useful here
static void
set_environ_vars(char **eargv, int eargc)
{
	char key[BUFLEN];
	char value[BUFLEN];
	for (int i = 0; i < eargc; i++) {
		get_environ_key(eargv[i], key);
		get_environ_value(eargv[i], value, block_contains(eargv[i], '='));

		if (setenv(key, value, 1) < 0) {
			perror(SETENV_ERROR);
		}
	}
}


// opens the file in which the stdin/stdout/stderr
// flow will be redirected, and returns
// the file descriptor
//
// Find out what permissions it needs.
// Does it have to be closed after the execve(2) call?
//
// Hints:
// - if O_CREAT is used, add S_IWUSR and S_IRUSR
// 	to make it a readable normal file
static int
open_redir_fd(char *file, int flags)
{
	int file_descriptor;
	if (flags & O_CREAT) {
		file_descriptor = open(file, flags, S_IWUSR | S_IRUSR);
	} else {
		file_descriptor = open(file, flags);
	}
	return file_descriptor;
}

bool
cd_error(char *cmd)
{
	if (strncmp(cmd, "cd", 2) == 0) {
		fprintf(stderr, "exec failed : No such file or directory\n");
		return true;
	}

	return false;
}

// executes a command - does not return
//
// Hint:
// - check how the 'cmd' structs are defined
// 	in types.h
// - casting could be a good option
void
exec_cmd(struct cmd *cmd)
{
	// To be used in the different cases
	struct execcmd *e;
	struct backcmd *b;
	struct execcmd *r;
	struct pipecmd *p;

	switch (cmd->type) {
	case EXEC: {
		e = (struct execcmd *) cmd;
		if (e->argv[0] && cd_error(e->argv[0])) {
			_exit(EXIT_FAILURE);
		}

		set_environ_vars(e->eargv, e->eargc);
		execvp(e->argv[0], e->argv);
		// perror("exec failed ");
		_exit(EXIT_FAILURE);
		break;
	}
	case BACK: {
		b = (struct backcmd *) cmd;
		exec_cmd(b->c);
		_exit(EXIT_FAILURE);
		break;
	}

	case REDIR: {
		// changes the input/output/stderr flow
		//
		// To check if a redirection has to be performed
		// verify if file name's length (in the execcmd struct)
		// is greater than zero
		//
		r = (struct execcmd *) cmd;
		char *temp = r->scmd;
		char *pos;
		while ((pos = strpbrk(temp, "<>")) != NULL) {
			if (*pos == '<') {
				manejo_de_archivos(r->in_file,
				                   O_RDONLY,
				                   STDIN_FILENO);
			} else {
				if (pos > r->scmd && *(pos - 1) == '2' &&
				    pos[1] == '&' && pos[2] == '1') {
					if (dup2(STDOUT_FILENO, STDERR_FILENO) <
					    0) {
						perror(DUP_ERROR);
						_exit(EXIT_FAILURE);
					}
				} else if (pos > r->scmd && *(pos - 1) == '2') {
					manejo_de_archivos(r->err_file,
					                   O_WRONLY | O_CREAT,
					                   STDERR_FILENO);
				} else {
					manejo_de_archivos(r->out_file,
					                   O_WRONLY | O_CREAT |
					                           O_TRUNC,
					                   STDOUT_FILENO);
				}
			}
			temp = pos + 1;
		}

		r->type = EXEC;
		cmd = (struct cmd *) r;
		exec_cmd(cmd);
		break;
	}

	case PIPE: {
		// pipes two commands
		//
		p = (struct pipecmd *) cmd;
		int fd[2];
		int pid_1, pid_2;
		if (pipe(fd) == -1) {
			perror(PIPE_ERROR);
			_exit(EXIT_FAILURE);
		}

		pid_1 = fork();
		if (pid_1 == -1) {
			perror(FORK_ERROR);
			_exit(EXIT_FAILURE);
		}
		if (pid_1 == 0) {
			setpgid(0, 0);
			close(fd[READ]);
			dup2(fd[WRITE], STDOUT_FILENO);
			close(fd[WRITE]);

			exec_cmd(p->leftcmd);

			perror(LEFT_ERROR);
			_exit(EXIT_FAILURE);
		}

		pid_2 = fork();
		if (pid_2 == -1) {
			perror(FORK_ERROR);
			_exit(EXIT_FAILURE);
		}
		if (pid_2 == 0) {
			setpgid(0, 0);
			close(fd[WRITE]);
			dup2(fd[READ], STDIN_FILENO);
			close(fd[READ]);

			exec_cmd(p->rightcmd);

			perror(RIGTH_ERROR);
			_exit(EXIT_FAILURE);
		}

		close(fd[READ]);
		close(fd[WRITE]);

		int status1, status2;
		if (waitpid(pid_1, &status1, 0) < 0 ||
		    waitpid(pid_2, &status2, 0) < 0) {
			perror(WPID_ERROR);
		}
		int exit1;
		if (WIFEXITED(status2)) {
			exit1 = WEXITSTATUS(status2);
		} else {
			exit1 = 1;
		}
		free_command(parsed_pipe);
		_exit(exit1);

		break;
	}
	}
}
