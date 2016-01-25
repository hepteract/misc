#Embedded file name: name\__init__.pyc
from leviathans import int_to_roman
import itertools, pickle, random, types, string

prefixes = ('El', 'Sh', 'A', 'Fre', 'Ra', 'La', 'Le', 'Fra', 'How')
sounds = ('sh', 'ch', 'i', 'ah', 'ie', 'l', 'a', 'h', 'it')
suffixes = ('ah', 'ed', 'ie', 'zer', 'tor', 'a', 't')
censorable = pickle.load(open('censor.dat'))

import markov

#prefixes = sounds = suffixes = lambda name = None: [''.join(itertools.islice(chain, 3))]

def censor(text):
    for censored in censorable:
        if censored in text.lower():
            return False

    return text


def name_legacy(max_mid = 3):
    _name = random.choice(prefixes)
    for i in xrange(random.randrange(1, max_mid)):
        _name += random.choice(sounds)

    _name += random.choice((random.choice(suffixes), ''))
    if censor(_name):
        return _name
    return name()

def generate_legacy(sep = ' ', prefix = prefixes, body = sounds, bodies = 1, _terminate = None, suffix = suffixes, terminate = None):
    if type(prefix) == types.FunctionType:
        name = random.choice(prefix(''))
    else:
        name = random.choice(prefix)
    name += sep
    
    for i in xrange(bodies):
        if type(body) == types.FunctionType:
            name += random.choice(body(name))
        else:
            name += random.choice(body)
        name += sep

    if _terminate != None:
        name += sep
        if type(_terminate) == tuple or type(_terminate) == list:
            name += random.choice(_terminate)
        else:
            name += str(_terminate)
        name += sep
    if type(suffix) == types.FunctionType:
        suffix = suffix(name)
    name += random.choice(suffix)
    if terminate != None:
        name += sep
        raw_input(terminate)
        name += terminate
    if censor(name):
        return name
    else:
        random.seed()
        return generate(sep, prefix, body, bodies, suffix)
    if censor(name):
        return name
    return generate(sep, prefix, body, bodies, suffix)

def generate(*args, **kwargs):
    num = random.randrange(3, 5)
    if "bodies" in kwargs:
        num += kwargs["bodies"]
        
    if "chain" in kwargs:
        src = kwargs["chain"]
    else:
        src = markov.chain_japanese
        
    name = ''.join(itertools.islice(src, num)).capitalize()
    if "suffix" in kwargs:
        name += random.choice( kwargs["suffix"](name) )
        
    return name

def name(max_mid = 3):
    return generate(bodies = random.randrange(1, max_mid))

def element_name(min_len = 6, max_len = 10):
    name = ""
    chain = iter(markov.chain_periodic)
    while not name.endswith("\n"):
        name += next(chain)
        
    if len(name) < min_len or len(name) > max_len or not censor(name):
        return element_name(min_len, max_len)
    return name[:-1].capitalize()

romans = {}

def romanize(name):
    if name in romans:
        romans[name] += 1
        return (int_to_roman(romans[name]),)
    else:
        romans[name] = 1
        return ('I', '')


latins = {}
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def alphabetize(name):
    if name in latins:
        latins[name] += 1
        return alphabet[latins[name]]
    else:
        latins[name] = 1
        return ('A', 'Prime')


def postfix_func(postfix, suffix):
    return lambda name: (postfix + random.choice(suffix(name)),)


suffix_tools = {'alphabet': latins,
 'roman': romans}

def seed():
    for suffix_tool in suffix_tools:
        suffix_tools[suffix_tool] = {}
