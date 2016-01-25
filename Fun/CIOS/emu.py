#!/usr/bin/python
import emulib
import random
import time
import sys
import os

print("emucios v0.1.6 starting")
time.sleep(1)

emulib.load("chipsets")
emulib.load("memory")
emulib.load("outputs")
emulib.load("devices")
emulib.load("data")
emulib.load("kernel")
emulib.load("drivers")
emulib.load("UI")
emulib.load("portals")
emulib.load("ROM")

import rom

emulib.buffer("Booting ROM...")

rom.boot()
