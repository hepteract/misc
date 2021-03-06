#!/usr/bin/python2.7

import marshal
import struct
import sys
import bz2
import os

_compile = compile

_constants = []
_macros = {}

def parse_macro(macro, args):
    code = macro
    for index, value in enumerate(args, 1):
        code = code.replace("%" + str(index), value)
    code = code.replace("%a", " ".join(args))
    return code

def process_source(code):
    lines = code.split("\n")

    for line in lines:
        line = line.replace("%nop;", "").replace("&newline;", "\n")
        if line.startswith("#include "):
            with open(line.replace("#include ", "")) as f:
                include = f.read()
            code = code.replace( line, process_source(include) )
        elif line.startswith("#define "):
            index = 1
            while line.split(" ")[index].endswith("\\"):
                temp = line.split(" ")
                temp[index] = temp[index][:-1]
                line = " ".join(temp)
                index += 1
            index += 1
            _constants.append((" ".join( line.split(" ")[1:index] ),\
                              " ".join( line.split(" ")[index:] )))
        elif line.startswith("#macro "):
            index = 1
            while line.split(" ")[index].endswith("\\"):
                temp = line.split(" ")
                temp[index] = temp[index][:-1]
                line = " ".join(temp)
                index += 1
            index += 1
            _macros[" ".join( line.split(" ")[1:index] )] = \
                              " ".join( line.split(" ")[index:] )

    for constant in _constants:
        code = code.replace(constant[0], constant[1])

    lines = code.split("\n")

    for index, line in enumerate(lines, 0):
        temp = " ".join([x for x in line.split(" ") if x != ""])

        words = temp.split(" ")

        if words[0] in _macros:
            lines[index] = line.replace(temp, parse_macro(_macros[ words[0] ], words[1:]))
        
    return "\n".join(lines)

def _compile_string(source, filename):
    source = process_source(source)
    
    code = _compile(source, filename, "exec")
    #code = marshal.dumps(code)

    return code

def compile_string(source, filename, data = "\x00"):
    path = os.path.abspath(os.path.join(*__file__.split("/")[:-1] + ["parser.py"]))
    
    if type(source) is dict:
        bytes = bz2.compress(marshal.dumps( (source, data) ))
    else:
        code = _compile_string(source, filename)
        bytes = bz2.compress(marshal.dumps( ({"__main__" : code}, data) ))

    bytecode = "\x00LOVE" + bytes

    return bytecode

def compile(sources, filename, data = "\x00", stub = ""):
    if type(sources) is dict:
        source = {}
        for name, code in sources.items():
            source[name] = _compile_string(code, name)
    else:
        source = sources
        
    code = compile_string(source, filename.split("/")[-1], data)

    with open(filename, 'w') as f:
        f.write(stub)
        f.write(code)

def make(source, filename, data = "\x00"):
    if data != "":
        with open(data) as f:
            data = f.read()
    with open(source) as f:
        source = f.read()

    with open("/home/elijah/Coding/PyExec/stub") as f:
        stub = f.read()

    compile(source, filename, data, stub)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        make(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        make(sys.argv[1], sys.argv[1].replace(".py", ""))
    else:
        print "No arguments"
