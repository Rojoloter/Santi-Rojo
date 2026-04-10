#include <inc/lib.h>

void
umain(int argc, char **argv)
{
	int myid = sys_getenvid();
	int prio = sys_env_get_priority(myid);

	cprintf("[TEST] Iniciado con prioridad %d (PID: %08x)\n", prio, myid);

	cprintf("[TEST] Intentando AUMENTAR prioridad a %d...\n", prio + 2);
	sys_env_set_priority(myid, prio + 2);

	int new_prio = sys_env_get_priority(myid);
	cprintf("[TEST] Prioridad actual luego del intento: %d\n", new_prio);

	cprintf("[TEST] Intentando REDUCIR prioridad a %d...\n", prio - 1);
	sys_env_set_priority(myid, prio - 1);

	new_prio = sys_env_get_priority(myid);
	cprintf("[TEST] Prioridad actual luego de reducir: %d\n", new_prio);

	cprintf("[TEST] Finalizado.\n");
}
