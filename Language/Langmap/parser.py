#!/usr/bin/python3.4

import re

class Parser(object):
    def __init__(self, scope = None):
        self.scope = scope or {}

        self.grammar = (
("call", re.compile(r' *(\w+)\((["\w, ]*)\) *')),
            )
        self.expressions = (
(str, re.compile(r'"(\w*)"')),
(int, re.compile(r'([0123456789]+)')),
            )

    def tokenize_line(self, code):
        for token, regex in self.grammar:
            match = regex.match(code)
            if match:
                return token, match

    def tokenize(self, code):
        lines = code.replace("\n", " ").replace("\t", " ").split(";")

        return [val for val in\
                [self.tokenize_line(line) for line in lines] if val]

    def parse_expression(self, expr):
        for type, regex in self.expressions:
            match = regex.match(expr)
            if match:
                return type(match.group(1))

    def parse_tokens(self, tokens):
        for token, match in tokens:
            if token == "call":
                expr = match.group(2).split(',')
                self.scope[match.group(1)](*[self.parse_expression(exp) for exp in expr])

    def parse(self, code):
        return self.parse_tokens( self.tokenize(code) )
        
