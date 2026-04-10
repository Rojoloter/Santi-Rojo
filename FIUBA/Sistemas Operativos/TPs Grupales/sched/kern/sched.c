#include <inc/assert.h>
#include <inc/x86.h>
#include <kern/spinlock.h>
#include <kern/env.h>
#include <kern/pmap.h>
#include <kern/monitor.h>

#include "../inc/env.h"

static int sched_calls = 0;
static envid_t execution_history[1024];
static int history_index = 0;
static int env_run_counts[NENV] = { 0 };

void sched_halt(void);

// Choose a user environment to run and run it.
void
sched_yield(void)
{
#ifdef SCHED_ROUND_ROBIN
	// Implement simple round-robin scheduling.
	//
	// Search through 'envs' for an ENV_RUNNABLE environment in
	// circular fashion starting just after the env this CPU was
	// last running. Switch to the first such environment found.
	//
	// If no envs are runnable, but the environment previously
	// running on this CPU is still ENV_RUNNING, it's okay to
	// choose that environment.
	//
	// Never choose an environment that's currently running on
	// another CPU (env_status == ENV_RUNNING). If there are
	// no runnable environments, simply drop through to the code
	// below to halt the cpu.

	if (curenv == NULL && envs[0].env_status == ENV_RUNNABLE) {
		env_run(&envs[0]);
	}

	int indice_actual = 0;
	while (curenv != NULL && envs[indice_actual].env_id != curenv->env_id) {
		indice_actual++;
	}

	int indice = indice_actual + 1;
	while (indice != indice_actual) {
		if (envs[indice].env_status == ENV_RUNNABLE) {
			env_run(&envs[indice]);
		}
		indice++;

		if (indice == NENV) {
			indice = 0;
		}
	}

	if (curenv != NULL && curenv->env_status == ENV_RUNNING) {
		env_run(curenv);
	}
#endif

#ifdef SCHED_PRIORITIES
	// Implement simple priorities scheduling.
	//
	// Environments now have a "priority" so it must be consider
	// when the selection is performed.
	//
	// Be careful to not fall in "starvation" such that only one
	// environment is selected and run every time.

	static int boost_counter = 0;
	const int boost_interval = 30;
	sched_calls++;

	boost_counter++;
	if (boost_counter >= boost_interval) {
		for (int i = 0; i < NENV; i++) {
			if (envs[i].env_status == ENV_RUNNABLE) {
				envs[i].env_priority++;
			}
		}
		boost_counter = 0;
	}
	struct Env *next_env = NULL;
	int max_priority = -1;


	for (int i = 0; i < NENV; i++) {
		if (envs[i].env_status == ENV_RUNNABLE &&
		    envs[i].env_priority > max_priority) {
			max_priority = envs[i].env_priority;
			next_env = &envs[i];
		}
	}

	if (next_env) {
		// Para el historial de procesos ejecutados/seleccionados
		if (history_index < 1024) {
			execution_history[history_index++] = next_env->env_id;
		}

		// Para el Número de ejecuciones por cada proceso
		int next_env_index = ENVX(next_env->env_id);
		env_run_counts[next_env_index]++;

		if (next_env->env_priority > 1) {
			next_env->env_priority--;
		}
		env_run(next_env);
	} else if (curenv && curenv->env_status == ENV_RUNNING) {
		env_run(curenv);
	}
#endif

	// sched_halt never returns
	sched_halt();
}

// Halt this CPU when there is nothing to do. Wait until the
// timer interrupt wakes it up. This function never returns.
//
void
sched_halt(void)
{
	int i;

	// For debugging and testing purposes, if there are no runnable
	// environments in the system, then drop into the kernel monitor.
	for (i = 0; i < NENV; i++) {
		if ((envs[i].env_status == ENV_RUNNABLE ||
		     envs[i].env_status == ENV_RUNNING ||
		     envs[i].env_status == ENV_DYING))
			break;
	}
	if (i == NENV) {
		cprintf("No runnable environments in the system!\n");

		// Once the scheduler has finishied it's work, print statistics
		// on performance.
		cprintf("\n Scheduling Statistics: \n");
		cprintf("Total scheduler calls: %d\n", sched_calls);
		cprintf("Execution history of the last %d enviroment/s: \n",
		        history_index);
		cprintf("[0] start -> %08x\n", execution_history[0]);
		for (int j = 1; j < history_index; j++) {
			cprintf("[%d] %08x -> %08x\n",
			        j,
			        execution_history[j - 1],
			        execution_history[j]);
		}
		cprintf("Enviroment execution counts: \n");
		for (int j = 0; j < NENV; j++) {
			if (env_run_counts[j] > 0) {
				cprintf("[%d] env_id %08x: %d executions \n",
				        j,
				        envs[j].env_id,
				        env_run_counts[j]);
			}
		}

		while (1)
			monitor(NULL);
	}

	// Mark that no environment is running on this CPU
	curenv = NULL;
	lcr3(PADDR(kern_pgdir));

	// Mark that this CPU is in the HALT state, so that when
	// timer interupts come in, we know we should re-acquire the
	// big kernel lock
	xchg(&thiscpu->cpu_status, CPU_HALTED);

	// Release the big kernel lock as if we were "leaving" the kernel
	unlock_kernel();

	// Reset stack pointer, enable interrupts and then halt.
	asm volatile("movl $0, %%ebp\n"
	             "movl %0, %%esp\n"
	             "pushl $0\n"
	             "pushl $0\n"
	             "sti\n"
	             "1:\n"
	             "hlt\n"
	             "jmp 1b\n"
	             :
	             : "a"(thiscpu->cpu_ts.ts_esp0));
}
