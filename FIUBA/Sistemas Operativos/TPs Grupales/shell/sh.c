#include "defs.h"
#include "types.h"
#include "readline.h"
#include "runcmd.h"

char prompt[PRMTLEN] = { 0 };

/*
 *Se ejecuta automáticamente cuando termina un proceso hijo.
 *waitpid(0, &stat_loc, WNOHANG); lo que hace es esperar por cualquier proceso
 *hijo del mismo grupo de procesos. Retorna el pid del proceso terminado, o 0 si
 *no hay ninguno. Por eso si siguen habiendo procesos hijos, hay que esperar a
 *que terminen e indicar su PID
 */

static void
sigchld_handler()
{
	int stat_loc;
	int pid = waitpid(0, &stat_loc, WNOHANG);
	while (pid > 0) {
		// Adentro del while se pasa el PID de int a string, para evitar usar snprintf y solo escribir con write
		char buffer[64];
		int pos = 0;
		for (int i = 0; i < 19; i++) {
			const char *msg = "==> terminado: PID=";
			buffer[pos++] = msg[i];
		}
		char pid_str[16];
		int pid_len = 0;
		while (pid > 0) {
			pid_str[pid_len++] = (pid % 10) + '0';
			pid /= 10;
		}
		for (int i = pid_len - 1; i >= 0; i--) {
			buffer[pos++] = pid_str[i];
		}
		buffer[pos++] = '\n';
		buffer[pos++] = '$';
		buffer[pos++] = ' ';

		ssize_t res = write(STDOUT_FILENO, buffer, pos);
		if (res == -1) {
			perror("Sigchld");
			exit(EXIT_FAILURE);
		}
		pid = waitpid(0, &stat_loc, WNOHANG);
	}
}

/*
 *Acá se configura el sistema para que maneje la señal SIGCHLD como la definimos anteriormente
 */
static void
sigaction_init()
{
	struct sigaction act = { 0 };
	act.sa_handler = sigchld_handler;
	act.sa_flags = SA_RESTART | SA_NOCLDSTOP;  // REVISAR LAS FLAGS
	int res = sigaction(SIGCHLD, &act, NULL);
	if (res == -1) {
		perror("sigaction");
		exit(EXIT_FAILURE);
	}
}
// runs a shell command
static void
run_shell()
{
	char *cmd;

	while ((cmd = read_line(prompt)) != NULL)
		if (run_cmd(cmd) == EXIT_SHELL)
			return;
}

// initializes the shell
// with the "HOME" directory
static void
init_shell()
{
	sigaction_init();
	char buf[BUFLEN] = { 0 };
	char *home = getenv("HOME");

	if (chdir(home) < 0) {
		snprintf(buf, sizeof buf, "cannot cd to %s ", home);
		perror(buf);
	} else {
		snprintf(prompt, sizeof prompt, "(%s)", home);
	}
}

int
main(void)
{
	init_shell();

	run_shell();

	return 0;
}
