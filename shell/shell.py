#! /usr/bin/env python3

import os, sys, time, re

while 1:
    userInput = input(os.getcwd() + "$")
    userArgs = userInput.split(" ")

    # if user doesn't input anything, we prompt again
    if "" in userArgs:
        continue


    # end shell if user enters exit
    if 'exit' in userArgs:
        sys.exit(-1)

    # change directory when cd is in userArgs
    if 'cd' in userArgs:
        if '..' in userArgs:
            dirChange = '..'
        else:
            dirChange = userArgs[0]
            try:
                os.chdir(dirChange) # attempt to change dir

            except FileNotFoundError:
                pass

            continue

        
    pid = os.getpid()
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:

        os.write(1, ("Child: pid ==%d. Parent: pid=%d\n" %(os.getpid(), pid)).encode())
            
    else:
        os.write(1, ("Parent: pid=%d. Child's pid = %d\n" %(pid, rc)).encode())
        childPid = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %childPid).encode())
                
