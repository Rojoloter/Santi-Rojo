// prioridad media
#include <inc/lib.h>

void
umain(int argc, char **argv)
{
	envid_t pid = sys_getenvid();
	int res = sys_env_set_priority(pid, 3);
	int prio = sys_env_get_priority(pid);
	cprintf("[MID] Proceso de MEDIA prioridad iniciado (PID:%08x) con "
	        "prioridad %d\n",
	        pid,
	        prio);
	for (int i = 0; i < 5; i++) {
		prio = sys_env_get_priority(pid);
		cprintf("[MID] Iteración %d, Prioridad %d\n", i, prio);
		sys_yield();
	}
	cprintf("[MID] Finalizado.\n");
}