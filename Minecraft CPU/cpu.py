#!/usr/bin/env python3

# Registers
rA = 0
rB = 0
rC = 0
rD = 0
rE = 0
rF = 0
# End registers

def add():
	global rC
	rC = rA
	rC += rB

def sub():
	global rC
	rC = rA
	rC -= rB

def mul():
	global rC
	rC = rA
	rC *= rB

def div():
	global rC
	rC = rA
	rC /= rB

def mod():
	global rC
	rC = rA
	rC %= rB

def min():
	global rC
	rC = rA
	rC = min(rC, rB)

def max():
	global rC
	rC = rA
	rC = max(rC, rB)
