#!/usr/bin/python2

import sys

def _trace(frame, event, arg):
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno

    print filename, f_lineno
    frame.f_lineno = input("Goto: ")
