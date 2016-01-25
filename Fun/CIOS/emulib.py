import random
import time
import sys
import os

def buffer(text):
    print text, '\r',
    sys.stdout.flush()
    time.sleep(random.random() * 3)
    print "\t\t\t\t\t[ OK ]"

def load(text):
    buffer("Loading " + text + "...")
