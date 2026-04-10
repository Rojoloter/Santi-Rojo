// prioridad baja
#include <inc/lib.h>

void
umain(int argc, char **argv)
{
	envid_t pid = sys_getenvid();
	int res = sys_env_set_priority(pid, 1);
	int prio = sys_env_get_priority(pid);
	cprintf("[LOW] Proceso de BAJA prioridad iniciado (PID:%08x) con "
	        "prioridad %d\n",
	        pid,
	        prio);

	for (int i = 0; i < 5; i++) {
		prio = sys_env_get_priority(pid);
		cprintf("[LOW] Iteración %d, Prioridad %d\n", i, prio);
		sys_yield();
	}
	cprintf("[LOW] Finalizado.\n");
}