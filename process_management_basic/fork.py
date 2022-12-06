#!/usr/bin/python3

import os, sys

print("os.fork() before")
ret = os.fork()
print("os.fork() after")

if ret == 0:
    print("子プロセス: pid={}, 親プロセス: pid={}".format(os.getpid(), os.getppid()))
elif ret > 0:
	print("親プロセス: pid={}, 子プロセス: pid{}".format(os.getpid(), ret))

sys.exit(1)