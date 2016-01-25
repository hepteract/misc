# This module must be compiled into attack.pyc and cannot be imported directly
if __name__ != "attack": raise ImportError, __name__ + " does not support direct import"

MASK = MASK | _BASE

import random
import json

try:
    __exec__
except:
    with open("material.json") as matfile:
        materials = json.load(matfile)
    with open("weapon.json") as wepfile:
        weapons = json.load(wepfile)
    with open("character.json") as savfile:
        characters = json.load(savfile)
else:
    materials = __exec__["material"]
    characters = __exec__["character"]
    weapons = __exec__["weapon"]
    

for player in characters:
    characters[player]["tmp"] = characters[player]["stats"].copy()
    characters[player]["effects"] = {}

def roll(num):
    if type(num) is int:
        return random.randrange(0, num)
    else:
        return random.randrange(0, num[0]) + num[1]

def max_health(player):
    return characters[player]["stats"]["CON"] * 10 + 100

def _attack(offense, mat, sneak = False, off_dex = 0, off_str = 0, def_dex = 0, def_end = 0, weight = 0):
    dmg = 0

    defense = materials[mat]
    if type(offense) == dict:
    	attack = offense
    else:
        attack = weapons[offense]

    off_dex /= 1.5
    off_str /= 1.5
    def_dex /= 1.5
    def_end /= 0.5

    aim = attack['precision'] - (weight/2) - (def_dex) + (off_dex)
    if "pierce" in attack["class"]:
        if sneak:
            crit = roll(20) - (aim * 2)
            bonus = attack.get("sneak", 1)
        else:
            crit = roll(50) - aim
            bonus = 1

        if max(crit, 1) < defense['weakness']:
            dmg += ( roll(( attack["damage"], attack["bonus"] )) * attack["class"]["pierce"] ) * bonus
    hit = roll(20) + (aim / 4) + off_str - (def_end/2)

    base = roll(( attack["damage"], attack["bonus"] ))

    for atype in attack["class"]:
        if hit >= defense['resists'][atype] / 2:
            dmg += attack["class"][atype] * min ( (hit / max( defense['resists'][atype] , 1) ), 2) * base
    return dmg

def attack(player0, player1, sneak = False, do_dmg = False):    
    player0 = characters[player0]
    player1 = characters[player1]
    
    player0["tmp"] = player0["stats"].copy()

    dmg = _attack( player0["weapon"], player1["armor"], sneak, player0["tmp"]["DEX"], player0["tmp"]["STR"], player1["tmp"]["DEX"], player1["tmp"]["END"], materials[ player0["armor"] ]["weight"] + weapons[ player0["weapon"] ]["weight"])

    if do_dmg:
        player1["health"] -= dmg
        player1["health"] = max( player1["health"], 0 )

    return dmg
