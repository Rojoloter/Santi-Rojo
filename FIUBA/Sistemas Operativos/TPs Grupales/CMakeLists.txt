cmake_minimum_required(VERSION 4.0)
project(sisop_2025b_g57 C)

set(CMAKE_C_STANDARD 11)

include_directories(shell)

add_executable(sisop_2025b_g57
        shell/tests/reflector.c
        shell/builtin.c
        shell/builtin.h
        shell/createcmd.c
        shell/createcmd.h
        shell/defs.h
        shell/exec.c
        shell/exec.h
        shell/freecmd.c
        shell/freecmd.h
        shell/parsing.c
        shell/parsing.h
        shell/printstatus.c
        shell/printstatus.h
        shell/readline.c
        shell/readline.h
        shell/runcmd.c
        shell/runcmd.h
        shell/sh.c
        shell/types.h
        shell/utils.c
        shell/utils.h)
