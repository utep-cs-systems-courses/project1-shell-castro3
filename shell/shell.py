#! /usr/bin/env python3

import os, sys, re, fileinput

def parser(cmdString):
    outFile = None
    inFile = None
    cmd = ''

    cmdString = re.sub(' +', ' ', cmdString)

    if '>' in cmdString:
        [cmd, outFile] = cmdString.split('>',1)
        outFile = outFile.strip()

    if '<' in cmd:
        [cmd, inFile] = cmd.split('<', 1)
        inFile = inFile.strip()

    elif outFile != None and '<' in outFile:
        [outFile, inFile] = outFile.split('<', 1)

        outFile = outFile.strip()
        inFile = inFile.strip()

    else:
        cmd = cmdString

    return [cmd.split(), outFile, inFile]



while 1: #infinite loop that will keep us on the shell until user enters exit

    redirect = False
    if 'PS1' in os.environ:
        os.write(1, (os.getcwd() + '$ ').encode())
    else:
        os.write(1, (os.getcwd() + '$ ').encode())
        
    userInput = input()
    if '>' in userInput:
        redirect = True
    userInput = parser(userInput)
    print(userInput)

    # if user doesn't input anything, we prompt again
    if "" in userInput:
        continue


    # end shell if user enters exit
    if ['exit'] in userInput:
        os.write(1, ("Leaving shell...\n").encode())
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
            os.write(1, ("Directory does not exist!\n").encode())
            pass

        continue

        
    pid = os.getpid()
    rc = os.fork()
    pr,pw = os.pipe()

    for f in (pr, pw):
            os.set_inheritable(f, True)

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:

        if redirect:
            os.close(1)
            os.open(userInput[1], os.O_CREAT | os.O_WRONLY)
            os.set_inheritable(1, True)
        com = userInput
        for dir in re.split(":", os.environ['PATH']):
            pexec = "%s/%s" % (dir, com[0][0])
            os.write(1, ("Child: ...executing %s\n" % pexec).encode())
            try:
                os.execve(pexec, com[0], os.environ) #attempt to execute program
            except FileNotFoundError:
                pass

        os.write(2, ("Child: Cannot execute %s\n" % com[0]).encode())
        os.write(2, ("Command " + userInput[0] + " not found\n").encode())
        sys.exit(1)
            
    else:
        os.wait()




                       
