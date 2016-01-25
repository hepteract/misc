print "\nUSERSPACE HANDSHAKE IN PROGRESS\n"

import time, code, os

def switch():
    pyprmt = code.InteractiveConsole()
    pyprmt.push("from os import system as raw")
    
    print "Welcome to Doors on Python 2.7"
	
    input = "@print 'You are running PythonPrompt'"
    while not input in ("quit","exit"):
        if not input.startswith("@"):
            if os.system(input) != 32512:
                input = raw_input("> ")
                continue
        else:
            input = input[1:]
        
        pyprmt.push(input)
	
	input = raw_input("> ")

    print "\nGoing for shutdown..."
    time.sleep(3)
    exit()
