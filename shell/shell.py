#! /usr/bin/env python3

import os, sys, time, re

while 1: #infinite loop that will keep us on the shell until user enters exit

    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else:
        os.write(1, ('$ ').encode())
        
    userInput = input()
    userInput = userInput.split(" ")

    # if user doesn't input anything, we prompt again
    if "" in userInput:
        continue


    # end shell if user enters exit
    if 'exit' in userInput:
        os.write(1, ("Leaving shell...").encode())
        sys.exit(0)
        break

    # change directory when user enters cd
    if 'cd' in userInput:
        if '..' in userInput:
            dirChange = '..'
        else:
            dirChange = userInput[1]

        try:
            os.chdir(dirChange) # attempt to change dir
            os.write(1, (os.getcwd()).encode())
        except FileNotFoundError:
            os.write(1, ("Directory does not exist!").encode())
            pass

        continue
        
        
    pid = os.getpid()
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:

        com = userInput
        for dir in re.split(":", os.environ['PATH']):
            pexec = "%s/%s" % (dir, com[0])
            os.write(1, ("Child: ...executing %s\n" % pexec).encode())
            try:
                os.execve(pexec, com, os.environ) #attempt to execute program
            except FileNotFoundError:
                pass

        os.write(2, ("Child: Cannot execute %s\n" % com[0]).encode())
        sys.exit(1)
            
    else:
        os.wait()
    
def parser(userInput):
    outFile = None
    inFile = None
    input = ""

    userInput = re.sub(' +', '', userInput)

    if '>' in userInput:
        [input, inFile] = input.split('<', 1)
        inFile = inFile.strip()

    elif outFile != None and '<' in outFile:
        [outFile, inFile] = outFile.split('<', 1)

        outFile = outFile.strip()
        inFile = inFile.strip()

    return input.split(), outFile, inFile





                       
