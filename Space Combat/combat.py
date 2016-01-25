#!/usr/bin/python2.7

from __future__ import division

import collections
import json

class Shield(object):
    def __init__(self, strength, regen = 0, absorbtion = None,\
                 resists = {}, default = 0):
        self.max = self.str = float(strength)
        self.abs = absorbtion
        self.reg = regen
        
        self.res = collections.defaultdict(self.generic_resist)
        self.res.update(resists)
        self.default = default

        if self.abs is None:
            self.abs = 0.3 * self.max

    @property
    def mul(self):
        if self.str == 0:
            return 0
        else:
            return min( 1, ((self.str + self.abs) / self.max ) )

    def calculate(self, dmg, pen = False, energy = True, type = None):
        bleed = dmg

        dmg *= self.mul

        dmg *= ((0.0 - self.res[type]) / 100) + 1 # resist 0 is no resist, resist 100 is full resist

        if dmg > bleed:
            bleed /= 2
        else:
            bleed -= dmg
            
        return max(dmg, 0), max(bleed, 0)

    def dmg(self, dmg):
        damage, bleed = self.calculate(dmg)
        self.str = max(self.str - damage, 0)
        return bleed

    def generic_resist(self):
        return self.default

    def update(self):
        self.str = min(self.max, self.str + self.regen)

class Ship(object):
    def __init__(self, hp, shield):
        if type(shield) is int:
            self.shield = Shield(shield)
        else:
            self.shield = shield

        self.hp = hp

    @property
    def shp(self):
        return self.shield.str

    @property
    def hhp(self):
        return self.hp

    def dmg(self, dmg):
        self.hp -= self.shield.dmg(dmg)

    def update(self):
        self.shield.update()

class Shipyard(object):
    def __init__(self, string):
        self.ships = json.loads(string)

    def __getitem__(self, name):
        ship = collections.defaultdict(lambda:None)
        ship.update( self.ships[name] )

        shield = Shield(ship["str"], ship["reg"] if ship["reg"] else 0,\
            ship["abs"], ship["res"] if ship["res"] else {},\
            ship["default"] if ship["default"] else 0)
        return Ship(ship["hp"], shield)
