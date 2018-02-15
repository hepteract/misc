#!/usr/bin/env python2

import leviathans_world as game
import leviathans_planets as lp

game.modules = []

with open("modules.conf") as conf:
    modules = conf.readlines()
    for module in modules:
        if module.startswith("#"):
            continue
        elif module.startswith("*"):
            module = module[1:]
        else:
            module = "leviathans_" + module
        game.modules.append(__import__(module[:-1]))

if __name__ != "__main__":
    raise ImportError("leviathans_main does not support being imported!")
else:
    lp.main()
