// prioridad alta
#include <inc/lib.h>

void
umain(int argc, char **argv)
{
	envid_t pid = sys_getenvid();
	int prio = sys_env_get_priority(pid);
	cprintf("[HIGH] Proceso de ALTA prioridad iniciado (PID:%08x) con "
	        "prioridad %d\n",
	        pid,
	        prio);
	for (int i = 0; i < 5; i++) {
		prio = sys_env_get_priority(pid);
		cprintf("[HIGH]Iteración %d, Prioridad %d\n", i, prio);
		sys_yield();
	}
	cprintf("[HIGH] Finalizado.\n");
}