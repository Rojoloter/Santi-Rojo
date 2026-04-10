#ifndef NARGS
#define NARGS 4
#endif
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

void
error_args()
{
	fprintf(stderr, "Argumentos no válidos.");
	exit(1);
}

void
error_pid()
{
	fprintf(stderr, "Error en la creación de un nuevo proceso");
	exit(1);
}

void
ejecutar(char *argumentos[])
{
	int pid = fork();
	if (pid == 0) {
		// Hijo
		execvp(argumentos[0], argumentos);
		perror("execvp");
		exit(1);
	} else if (pid > 0) {
		// padre
		wait(0);
	} else {
		error_pid();
	}
}

int
main(int argc, char *argv[])
{
	if (argc < 2) {
		error_args();
	}

	char *argumentos[NARGS + 2];  // Comando + argumentos + NULL
	argumentos[0] = argv[1];

	char *linea = NULL;
	size_t len = 0;
	ssize_t rd_res;
	int cargados = 0;
	while ((rd_res = getline(&linea, &len, stdin)) > 0) {
		if (linea[rd_res - 1] == '\n') {
			linea[rd_res - 1] = '\0';
		}
		argumentos[cargados + 1] = strdup(linea);
		cargados++;

		if (cargados == NARGS) {
			argumentos[cargados + 1] = NULL;
			ejecutar(argumentos);
			for (int i = 1; i <= cargados; i++) {
				free(argumentos[i]);
			}
			cargados = 0;
		}
	}

	if (cargados > 0) {  // Por si quedaron elementos < NARGS
		argumentos[cargados + 1] = NULL;
		ejecutar(argumentos);
		for (int i = 1; i <= cargados; i++) {
			free(argumentos[i]);
		}
	}
	free(linea);
	return 0;
}
