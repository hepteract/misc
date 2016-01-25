# This module must be compiled into attack.pyc and cannot be imported directly
if __name__ != "attack": raise ImportError, __name__ + " does not support direct import"

MASK = MASK | _ENEMIES

import collections
import random

def enemy_factory(enemies):
    enemies = enemies.values()
    def generate_enemy():
        return random.choice(enemies)
    return generate_enemy

_characters = characters
characters = collections.defaultdict( enemy_factory(_characters) )
characters.update(_characters)
