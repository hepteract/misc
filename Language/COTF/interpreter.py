#!/usr/bin/python2.7

from __future__ import print_function
from grako.contexts import Closure

import collections
import tokens
import sys

DEBUG = False

class _undefined(object):
    def cotf(self):
        return "undefined"
    
    __call__ = __getattr__ = __getitem__ = lambda self, *args, **kwargs: self
    __setitem__ = __setattr__ = lambda self, *args, **kwargs: None
    __bool__ = __eq__ = __lt__ = __gt__ = __le__ = __ne__ = __ge__ =\
               lambda self, *args, **kwargs: False
undefined = _undefined()
class _null(_undefined):
    def cotf(self):
        return '\x1b[A'
null = _null()

_eval = eval

class string(str):
    def __repr__(self):
        return "".join(('string("', str(self), '")'))
    def cotf(self):
        return repr(str(self))

class number(float):
    def __repr__(self):
        return "".join(('number(', str(self), ')'))
    def cotf(self):
        return str(self)
    def __str__(self):
        if int(self) == self:
            return str(int(self))
        else:
            return str(float(self))

class array(list):
    cotf = True
    def __getitem__(self, index):
        return clean(super(array, self).__getitem__(int(index)))
    def __setitem__(self, index, value):
        super(array, self).__setitem__(int(index), value)
    
    def __repr__(self):
        return "".join(("array", repr(tuple(self))))
    def cotf(self):
        return "".join(('(', " ".join([getattr(item, "cotf", lambda: "<unknown object>")() for item in self]), ')'))
    
    @property
    def length(self):
        return clean( len(self) )

def clean(value):
    if type(value) in (int, float, long):
        return number(value)
    elif type(value) in (str, unicode):
        return string(value)
    elif type(value) in (list, tuple, Closure):
        return array(value)
    elif value is True:
        return number(1)
    elif value is False:
        return number(0)
    else:
        return value

def evaluate(token, scope):
    if not token:
        return string("")
    
    if type(token) in (str, unicode):
        if token[0] in ("'", '"'):
            return string(token[1:-1])
        elif token[0] in "1234567890":
            return number(_eval(token))
        elif token == "()":
            return []
        else:
            return scope[token]
        
    elif type(token) in (list, tuple, Closure):
        return [eval(item, scope) for item in token]
    
    else:
        if token["op"]:
            data = [eval(item, scope) for item in token["input"]]
            return clean( _eval("".join((str(data[0]), token["op"], str(data[1])))) )
        elif token["not"]:
            return not eval(token["not"], scope)
        elif token["call"]:
            if DEBUG: print(len(token["arguments"]), token["arguments"])
            if token["arguments"] == u'()':
                return eval(token["call"], scope) ()
            elif type(token["arguments"]) not in (list, tuple, Closure):
                return eval(token["call"], scope) (eval(token["arguments"], scope))
            args = [eval(arg, scope) for arg in token["arguments"]]
            return eval(token["call"], scope) (*args)
        elif token["variable"]:
            scope[ token["variable"] ] = eval(token["value"], scope)
            return scope[ token["variable"] ]
        elif token["function"]:
            scope[ token["function"] ] = eval(token["value"], scope) ()
            return scope[ token["variable"] ]
        elif token["code"]:
            return CodeClass(token["code"], scope)
        elif token["func"]:
            return eval(token["func"], scope) ()
        elif token["getattr"]:
            ret = eval(token["getattr"], scope)
            
            attr = []
            for item in token["get"]:
                if item[0] in "1234567890":
                    attr.append(_eval(item))
                else:
                    attr.append(item)
            
            for item in attr:
                try:
                    ret = ret[item]
                except:
                    try:
                        ret = getattr(ret, item)
                    except:
                        if DEBUG: print(ret, item)
                        return undefined
            return ret
                    
    return null

if DEBUG:
    def eval(token, scope):
        print(token, ":", scope)
        x = evaluate(token, scope)
        print(x)
        return x
else:
    eval = lambda *args, **kwargs: clean(evaluate(*args, **kwargs))

class CodeClass(object):
    def __init__(self, ast, scope = None, local = True):
        self.ast = ast
        self.scope = scope or {}
        self.local = local
        
    def __call__(self, *args, **kwargs):
        if self.local:
            scope = self.scope.copy()
        else:
            scope = self.scope

        return CodeObject(self.ast, scope)

    def cotf(self):
        return "<class>"

class CodeObject(object):
    def __init__(self, ast, scope = None):
        self.ast = ast
        if scope:
            self.scope = scope
        else:
            self.scope = collections.defaultdict(lambda *args, **kwargs: undefined)
            self.scope.update(builtins.builtins)

    def __call__(self, *args, **kwargs):
        self.scope.update(kwargs)
        self.scope["args"] = array(args)
        for token in self.ast:
            try:
                if token["return"]:
                    return eval(token["return"], self.scope)
                else:
                    eval(token, self.scope)
            except Exception, e:
                #print(e, sys.stderr)
                try:
                    eval(token, self.scope)
                except:
                    print("Uh oh! An error has occurred!", file = sys.stderr)
                    print(sys.exc_info()[0].__name__, ": ", sys.exc_info()[1], sep = '')
        if self.scope["return"] is not undefined:
            return self.scope["return"]
        return null

    def __getitem__(self, name):
        return self.scope[name]
    def __setitem__(self, name, value):
        self.scope[name] = value

    def cotf(self):
        return self.scope["__repr__"] if self.scope["__repr__"] is not undefined else "<code object>"

def handle_code(source, scope = None):
    if scope is None:
        scope = collections.defaultdict(lambda *args, **kwargs: undefined)
        scope.update(builtins.builtins)

    parser = tokens.grammarParser(parseinfo = False, eol_comments_re = "#.*?$")
    ast = parser.parse(source, 'root')
    return CodeObject(ast["code"], scope)

import builtins

def _exec(*args):
    code = compile("".join(args), "<cotf>", "single")
    _eval(code)
    return null

def main(filename = "test"):
    with open(filename) as f:
        source = f.read()

    scope = collections.defaultdict(lambda *args, **kwargs: undefined)
    scope.update(builtins.builtins)

    code = handle_code(source, scope)
    code(*sys.argv[1:])

    return code

def interact():
    scope = collections.defaultdict(lambda *args, **kwargs: undefined)
    scope.update(builtins.builtins)

    while True:
        try:
            code = raw_input("cotf> ")
        except EOFError:
            break

        if code.startswith("!"):
            obj = compile(code[1:], "<string>", "single")
            try:
                _eval( obj )
            except:
                print("Uh oh! An error has occurred!", file = sys.stderr)
                print(sys.exc_info()[0].__name__, ": ", sys.exc_info()[1], sep = '')
        else:
            if not code.endswith(";"):
                code = "print(repr(" + code + "));"
            handle_code(code, scope) (number(0), number(1), number(2), number(3))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        interact()
