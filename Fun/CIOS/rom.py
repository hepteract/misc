print "Massive Dynamic CIOS version 1.6 loaded"

import random
import time
import sys
import os

def boot():
    os.system("clear")
    time.sleep(1)
    print "Welcome to Massive Dynamic"
    print "You are running MD-CIOS v1.6"

    print "\n\n\n\n"
    time.sleep(4)

    print "We have detected that there may be something wrong with your graphics card."
    print "Defaulting to text output\n"
    
    time.sleep(4)

    data = "Detecting devices"
    for i in xrange(random.randrange(10,50)):
        print data, "\r",
        sys.stdout.flush()
        data += "."
        time.sleep(random.random())
    print "\n"

    print "Found sda"
    time.sleep(0.5)
    print "Found loop0"
    time.sleep(0.5)
    print "Found eth0"
    time.sleep(3)

    print "\n"

    data = "Detecting operating systems"
    for i in xrange(random.randrange(5,25)):
        print data, "\r",
        sys.stdout.flush()
        data += "."
        time.sleep(random.random())
    print "\n"

    print "Found one operating system - Doors\n"
    print "WARNING: No CIOS record found - defaulting to kernelboot"

    time.sleep(2)

    import kernel
