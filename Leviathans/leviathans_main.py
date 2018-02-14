#!/usr/bin/env python2

import leviathans_world as game
import leviathans_planets as lp

game.modules = []

with open("modules.conf") as conf:
    modules = conf.readlines()
    for module in modules:
        game.modules.append(__import__("leviathans_" + module[:-1]))

if __name__ != "__main__":
    raise ImportError("leviathans_main does not support being imported!")
else:
    lp.main()
