#!/usr/bin/python2.7

from __future__ import print_function
from interpreter import handle_code, null, undefined, string, number

import os

class PythonFunction(object):
    def cotf(self):
        return "".join(("<python function '", self.func.__name__, "'>"))
    def __repr__(self):
        return repr(self.func)
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        ret = self.func(*args, **kwargs)
        if hasattr(ret, "cotf"):
            return ret
        elif type(ret) is str:
            return string(ret)
        elif type(ret) in (int, float, long):
            return number(ret)
        return null
clean = PythonFunction

@PythonFunction
def _if(condition, code):
    if condition:
        code()

@PythonFunction
def _print(*args, **kwargs):
    _args = []
    for arg in args:
        if hasattr(arg, "cotf"):
            _args.append(str(arg))
        else:
            _args.append("<unknown object>")
    print(*_args, **kwargs)

@PythonFunction
def _repr(obj = null, *args):
    if hasattr(obj, "cotf"):
        return obj.cotf()
    else:
        return "<unknown object>"

@PythonFunction
def _import(name):
    if os.path.exists(name):
        with open(name) as f:
            code = f.read()
        code = handle_code(code)
        code()
        return code
    else:
        try:
            return __import__(name)
        except:
            return null

@PythonFunction
def get(obj, name):
    try:
        x = obj[name]
    except:
        return getattr(obj, name, undefined)
    if x in (undefined, null):
        return getattr(obj, name, undefined)
    return x

@PythonFunction
def set(obj, name, value):
    try:
        obj[name] = value
    except:
        setattr(obj, name, value)
    return value

_exit = exit
def exit(code = None):
    _exit(code)

builtins = {
            "input" : clean(raw_input),
            "exit" : clean(exit),

            "import" : _import,
            "print" : _print,
            "repr" : _repr,
            "get" : get,
            "set" : set,
            "if" : _if,
            
            "undefined" : undefined,
            "null" : null
           }

builtins_mod = _import("builtins")
if builtins_mod is not null:
    builtins.update(builtins_mod.scope)
