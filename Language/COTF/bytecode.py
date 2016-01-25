#!/usr/bin/python2.7

from grako.contexts import Closure

import interpreter
import marshal
import json

class Packager(object):
    """Base class for COTF bytecode packagers"""
    def extract(self, obj):
        if hasattr(obj, "ast"):
            return json.loads( json.dumps( obj.ast ) )
        else:
            return json.loads( json.dumps( obj ) )

class MarshalPackager(Packager):
    """Legacy packaging method that uses Python's built-in marshal module"""
    
    def dumps(self, obj):
        return marshal.dumps( self.extract(obj) )

    def dump(self, obj, file):
        marshal.dump( self.extract(obj), file )

    def loads(self, string, call = True):
        code = interpreter.CodeObject( marshal.loads(string) )
        if call: code()
        return code

    def load(self, file):
        code = interpreter.CodeObject( marshal.load(file) )
        if call: code()
        return code

legacy = MarshalPackager()

class COTFPackager(Packager):
    """Class written in pure Python that can pack and unpack COTF bytecode"""
    
    def dumps(self, obj):
        obj = self.extract(obj)

        return  "".join(( self._dump(obj)))

    def dump(self, obj, file):
        file.write(self.dumps(obj))

    def _dump(self, obj):
        if type(obj) is dict:
            string = "{"
            string += "\x1b".join( [self._dump(x) for x in obj.keys()] )
            string += "\x1b\x00"
            string += "\x1b".join( [self._dump(x) for x in obj.values()] )
            string += "\x1b\x01"
        elif type(obj) in (list, tuple, interpreter.array, Closure):
            string = "("
            string += "\x1b".join( [self._dump(x) for x in obj] )
            string += "\x1b\x01"
        elif type(obj) in (int, float, interpreter.number):
            string = "".join(("$", str(obj)))
        else:
            string = "".join(('"', str(obj)))
        return string

    def loads(self, string):
        type = string[0]
        string = string[1:]

        # List
        if type == "(":
            return self.handle_list(string)
            #return [self.loads(item) for item in string[:-1].split("\x1b")]
        elif type == "{":
            return self.handle_dict(string)
        elif type == '"':
            return interpreter.string( string )
        elif type == "$":
            try:
                return interpreter.number( string )
            except ValueError:
                return interpreter.number( int(string) )
        return None

    def handle_list(self, string):
        list = []
        last = ""
        i = 0
        while True:
            x = string[i]
            if x in ("\x01", "\x00"):
                if last != "":
                    list.append(self.loads(last))
                i += 1
                break
            elif x == "\x1b":
                if last != "":
                    list.append(self.loads(last))
                last = ""
            elif x == "(":
                while not last.endswith("\x01"):
                    i += 1
                    last += string[i]
                list.append(self.handle_list(last))
                last = ""
            else:
                last += x
            i += 1
        if len(string) > i:
            return list, string[i:]
        return list

    def handle_dict(self, string):
        names, remainder = self.handle_list(string)
        values = self.handle_list(remainder)
        return dict(zip(names, values))

cotf = COTFPackager()
