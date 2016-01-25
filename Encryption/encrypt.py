"""Simple homebrew pure-Python encryption library"""

import cPickle as pickle
import binascii

class Cipher(object):
    def __init__(self, key, recurse = True):
        if type(key) is str:
            key = key
        else:
            key = repr(key)
            
        self.key = tuple( [(pow(ord(char), len(key)) % 256) for char in key] )

    def encrypt(self, msg):
        out = []
        for index, char in enumerate(msg, 0):
            out.append(chr(( ord(char) + self.key[index % len(self.key)] ) % 256))
        return binascii.unhexlify(binascii.hexlify("".join(out))[::-1])

    def decrypt(self, msg):
        out = []
        for index, char in enumerate(msg, 0):
            out.append(chr(( ord(char) - self.key[index % len(self.key)] ) % 256))
        return binascii.unhexlify(binascii.hexlify("".join(out))[::-1])

ciphers = {}

def encrypt(key, msg):
    if key not in ciphers:
        ciphers[key] = Cipher(key)
    return ciphers[key].encrypt(msg)

def decrypt(key, msg):
    if key not in ciphers:
        ciphers[key] = Cipher(key)
    return ciphers[key].decrypt(msg)
