# This module must be compiled into attack.pyc and cannot be imported directly
if __name__ != "attack": raise ImportError, __name__ + " does not support direct import"

# This module depends on baseattack.py and must be compiled after it
if not MASK & _BASE: raise ImportError, __name__ + " depends on baseattack.py"

MASK = MASK | _MAGIC

try:
    __exec__
except:
    with open("magic.json") as magicfile:
        words = json.load(magicfile)
else:
    words = __exec__["magic"]

def decode(text):
    shout = text.split(" ")

    spell = words["nul"]

    for word in shout:
        if word in words:
            spell.update(words[word])

    return spell

prev_attack = attack
def attack(player0, player1, sneak = False, do_dmg = False, spell = None):
    if spell:        
        player0 = characters[player0]
        player1 = characters[player1]
        
        player0["tmp"] = player0["stats"].copy()
        
        for stat, effect in player0["effects"].items():
            player0["stats"][stat] = effect[0]
            if effect[1] <= 0:
                effect[1] -= 1
                player0["effects"][stat] = effect
            
        shout = decode(spell)

        for stat, val in shout["debuff"].items():
            if type(val) == int:
                player1["tmp"][stat] += val
            else:
                player1["effects"][stat] = val

        for stat, val in shout["stats"].items():
            if type(val) == int:
                player0["tmp"][stat] += val
            else:
                player0["effects"][stat] = val

        for dclass in shout["class"]:
            shout["class"][dclass] *= materials[player0["armor"]]["arcana"]
            shout["class"][dclass] *= 1 + (player0["tmp"]["INT"] / 5)

        dmg = _attack( shout, player1["armor"], sneak,\
            player0["tmp"]["INT"], player0["tmp"]["INT"],\
            player1["tmp"]["DEX"],player1["tmp"]["END"],\
            materials[ player0["armor"] ]["weight"] +\
            weapons[ player0["weapon"] ]["weight"])

        if do_dmg:
            player1["health"] -= dmg
            player1["health"] = max( player1["health"], 0 )

        return dmg

    else:
        return prev_attack(player0, player1, sneak, do_dmg)
