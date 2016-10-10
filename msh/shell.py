# -*- coding: utf-8 -*-

import os
import sys
import shlex
from msh.constants import *
from msh.builtins.cd import *

# SHELL_STATUS_RUN = 1
# SHELL_STATUS_STOP = 0
built_in_cmds = {}


def shell_loop():
    # start the loop here
    status = SHELL_STATUS_RUN
    while status == SHELL_STATUS_RUN:
        # display a command prompt
        sys.stdout.write('> ')
        sys.stdout.flush()
        # read command input
        cmd = sys.stdin.readline()
        # tokenize the command inpur
        cmd_tokens = tokenize(cmd)
        # execute the command and retrieve new status
        status = execute(cmd_tokens)


def main():
    init()
    shell_loop()


def init():
    register_command("cd", cd)


def register_command(name, func):
    built_in_cmds[name] = func


def tokenize(string):
    return shlex.split(string)


def execute(cmd_tokens):
    cmd_name = cmd_tokens[0]
    cmd_args = cmd_tokens[1:]
    if cmd_name in built_in_cmds:
        return built_in_cmds[cmd_name](cmd_args)

    pid = os.fork()
    if pid == 0:
        # child process
        # execute command
        os.execvp(cmd_tokens[0], cmd_tokens)
    elif pid > 0:
        # parent process
        while True:
            wpid, status = os.waitpid(pid, 0)
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break

    # return status indicating to wait for next command in shell_loop
    return SHELL_STATUS_RUN


if __name__ == "__main__":
    main()
