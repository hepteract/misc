#!/usr/bin/python2

import sys

def _trace(frame, event, arg):
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno

    print filename, lineno
    
    try:
        frame.f_lineno = input("Goto: ")
    except:
        print >> sys.stderr, type(sys.exc_info()[1]).__name__ + ":",  sys.exc_info()[1]

    return _trace

sys.settrace(_trace)

frame = sys._getframe().f_back
while frame:
    frame.f_trace = _trace
    frame = frame.f_back
