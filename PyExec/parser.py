#!/usr/bin/python2.7

import marshal
import struct
import types
import sys
import os

OVERRIDE_IMPORTS = False

raw_import = __import__

def generate_module(name, code, modules = {}, data = None):
    name = name.split(".")[0]
    module = types.ModuleType(name)

    module.__dict__["__exec__"] = data
    
    exec code in module.__dict__
    sys.modules[name] = module
    modules[name] = module
    return module

if OVERRIDE_IMPORTS:
    def import_handler(modules):
        def do_import(name, *args, **kwargs):
            if name in modules:
                return generate_module( modules[name] )
            else:
                return raw_import(name, *args, **kwargs)
        return do_import
else:
    def import_handler(modules):
        return __import__

def _original(f, arguments):
    codelen = struct.unpack("I", f.read(4))[0]
    code = f.read(codelen)
    data = f.read()

    obj = marshal.loads(code)
    scope = {"__exec__" : True}
    exec obj in scope
    if "main" in scope:
        scope["main"](f, data, arguments)

def _compress(f, arguments):
    raw = f.read().decode('bz2')

    codelen = struct.unpack("I", raw[:4])[0]
    code = raw[4:codelen + 4]
    data = raw[codelen + 4:]

    obj = marshal.loads(code)
    scope = {"__exec__" : True}
    exec obj in scope
    if "main" in scope:
        scope["main"](f, data, arguments)

def _marshal(f, arguments):
    decode = f.read().decode('bz2')
    raw = marshal.loads(decode)
    
    scope = {"__exec__" : True, "__builtins__" : __builtins__}
    scope["do_import"] = scope["__import__"] =\
                         scope["__builtins__"].__import__ =\
                         import_handler(raw[0])

    modules = {}

    for name, module in raw[0].items():
        generate_module(name, module, modules, raw[1])
    
    for name, module in modules.items():
        for name, value in module.__dict__.items():
            if name.endswith("main"):
                value(f, raw[1], arguments, modules)

versions = {"baby" : _original,
            "BABY" : _compress,
            "LOVE" : _marshal}

def _raise(f, args):
    raise IOError, "Invalid magic number"

def main(executable, arguments):
    f = open(executable)
    
    last = ""
    i = 0
    while last != "\x00" and i < 100:
        last = f.read(1)
        i += 1

    magic = f.read(4)

    versions.get(magic, _raise) (f, arguments)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Parser requires executable argument"
        exit()
    elif len(sys.argv) == 2:
        main(sys.argv[1], [])
    else:
        main(sys.argv[1], sys.argv[2:])
