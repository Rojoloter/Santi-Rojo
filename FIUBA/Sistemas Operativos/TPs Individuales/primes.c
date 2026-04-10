#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <stdio.h>

const int RD = 0;
const int WR = 1;

void
error_args()
{
	fprintf(stderr, "Argumentos no válidos.");
	exit(1);
}

void
error_pipe()
{
	fprintf(stderr, "Error en la creación del pipe");
	exit(1);
}

void
error_pid()
{
	fprintf(stderr, "Error en la creación de un nuevo proceso");
	exit(1);
}

void
error_wr(const int n)
{
	fprintf(stderr, "Error de escritura en %d", n);
	exit(1);
}

void
error_rd(const int n)
{
	fprintf(stderr, "Error de lectura en %d", n);
	exit(1);
}

void
primer_proceso(const int *pipe_ini, const int n)
{
	close(pipe_ini[RD]);
	for (int i = 2; i <= n; i++) {
		const ssize_t pipe_wr = write(pipe_ini[WR], &i, sizeof(i));
		if (pipe_wr < 0) {
			close(pipe_ini[WR]);
			error_wr(pipe_ini[WR]);
		}
	}
	close(pipe_ini[WR]);
	wait(0);
}


void
proceso_criba(const int *pipe_izq)
{
	close(pipe_izq[WR]);
	int primo;
	const ssize_t rd_res = read(pipe_izq[RD], &primo, sizeof(primo));
	if (rd_res < 0) {
		close(pipe_izq[RD]);
		error_rd(pipe_izq[RD]);
	} else if (rd_res == 0) {
		close(pipe_izq[RD]);
		exit(0);
	}
	printf("primo %d\n", primo);

	int pipe_der[2];
	const int res_pipe = pipe(pipe_der);
	if (res_pipe < 0) {
		error_pipe();
	}
	const int pid = fork();
	if (pid == 0) {
		close(pipe_izq[RD]);
		proceso_criba(pipe_der);
	} else if (pid > 0) {
		close(pipe_der[RD]);
		int leido;
		ssize_t res_rd = read(pipe_izq[RD], &leido, sizeof(leido));
		while (res_rd > 0) {
			if (leido % primo != 0) {
				const ssize_t res_wr =
				        write(pipe_der[WR], &leido, sizeof(leido));
				if (res_wr < 0) {
					close(pipe_der[WR]);
					close(pipe_izq[RD]);
					error_wr(pipe_der[WR]);
				}
			}
			res_rd = read(pipe_izq[RD], &leido, sizeof(leido));
		}
		close(pipe_der[WR]);
		close(pipe_izq[RD]);
		wait(0);
	} else {
		error_pid();
	}
}

int
main(int argc, char *argv[])
{
	if (argc != 2) {
		error_args();
	}
	int n = atoi(argv[1]);
	if (n < 2) {
		error_args();
	}
	int pipe_ini[2];
	const int pipe_res = pipe(pipe_ini);
	if (pipe_res < 0) {
		error_pipe();
	}
	const int pid = fork();
	if (pid == 0) {
		// hijo
		proceso_criba(pipe_ini);
	} else if (pid > 0) {
		// padre
		primer_proceso(pipe_ini, n);
	} else {
		error_pid();
	}
	return 0;
}