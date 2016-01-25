import leviathans_planets as lp
import leviathans_world as game

import binascii
import random

def dedupe(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

# Item IDs
UNKNOWN = 0x00
MISSILE = 0x01

class _CraftedItem(str):
    pass

def CraftedItem(name, components, itemid):
    obj = _CraftedItem(name)
    obj.comp = components
    obj.id = itemid

    return obj

@game.battle_hook
def fire_nuke(world, playerid, cmd, ship0, ship1):
    if "nuke" in cmd:
        player = world.players[playerid]

        for item in player.cargo:
            if type(item) is _CraftedItem:
                if item.id == MISSILE:
                    print "Firing nuclear warhead...\n"
                    for row in ship1.map:
                        for mod in row:
                            mod.dmg(1000)
                    player.cargo.remove(item)
                    return -1
        print "I'm sorry, Captain, but we do not have any nuclear missiles.\n"
        return -1

def get_item_name(comp):
    if ("warhead" in comp[0].lower() and "missile" in comp[1].lower())\
      or ("missile" in comp[0].lower() and "warhead" in comp[1].lower()):
        return (comp[0].replace(" missile", "").replace(" warhead", "") \
                + " nuclear missile", MISSILE)

    return ("Unknown Item", UNKNOWN)

def craft(world, cmd, playerid):
    player = world.players[playerid]

    ingredients = []

    for item in player.cargo:
        if item.lower() in cmd:
            ingredients.append(item)
            
    ingredients = dedupe(ingredients)
    try:
        ingredients.remove("")
    except ValueError:
        pass
    
    for item in ingredients:
        player.cargo.remove(item)

    name, itemid = get_item_name(ingredients)

    player.cargo.append(CraftedItem(name, ingredients, itemid))
    print name, "added.\n"

game.new_cmd["craft"] = craft

lp.blueprint_types.append("warhead")
lp.blueprint_types.append("missile")

def get_hash(string, max = None):
    if max is None:
        return int(binascii.hexlify(string), 16)
    else:
        return int(binascii.hexlify(string), 16) % max

# Material data format:
# (flags, radioactivity, hardness, value)
# Flags is a mask containing basic extra data
# Radioactivity affects missile damage and fuel potential
# Hardness is a simple scale measuring the effectiveness of the substance as armor
# Value measures how valued a material is (not used)

@game.world_hook
def generate_material_data(new, world):
    global material_data
    
    if not new:
        material_data = world.mat_data

    else:
        material_data = {}
        for mat in world.mat.keys():
            random.seed(get_hash(mat))

            values = []
            values.append(0x00)
            values.append(random.randrange(0, 20))
            values.append(random.randrange(0, 20))
            values.append(random.randrange(0, 20))
            
            material_data[mat] = values
        world.mat_data = material_data

for i in xrange(3):
    lp.blueprint_types.append("plate")

main = lp.main

if __name__ == "__main__":
    import leviathans_obc
    main()
