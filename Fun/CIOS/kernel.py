import random
import time
import sys
import os

def buffer(text):
    print text, '\r',
    sys.stdout.flush()
    time.sleep(random.random() * 1.5)
    print "\t\t\t\t\t[ OK ]"

def load(text):
    buffer("LOADING " + text.upper() + "...")

os.system("clear")

print "DOORS COFFEE V0.1"
load("drivers")
load("subnet")
load("nodes")
load("sockets")
load("ports")
load("filters")
load("daemons")
load("devices")
load("gateway")
load("proxy")
load("LAN")
load("network")
load("protocols")
load("memory")
load("scripts")
load("matrices")
load("modules")
load("code")
load("interpreter")
load("compiler")
load("hard drives")
load("particions")


load("userspace")
import userspace

print "SWITCHING TO USERSPACE..."
for i in xrange(5):
    time.sleep(1)
    print

userspace.switch()
