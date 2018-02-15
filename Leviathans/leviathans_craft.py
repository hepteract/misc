import leviathans_planets as lp
import leviathans_world as game

import logging
import binascii
import random

if __name__ != "__main__":
    logging.debug("leviathans_craft imported")

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
game.cmd_list["craft [items ...]"] = "combine items to create a crafted item"

def repair(world, cmd, playerid):
    player = world.players[playerid]

    mat = None
    plate = None
    for item in player.cargo:
        if item.endswith("plate") and item in world.blu.keys():
            mult = 1
            for prefix in game.item_prefix:
                if prefix in item:
                    mult = 2

            for material in world.mat_data.keys():
                if material in item:
                    plate = item
                    mat = world.mat_data[material][2] * mult
                    break

    if plate is None:
        print "No valid plates to repair with"
        return

    else:
        print "Plate chosen: %s (hardness %i)" % (plate, mat)

    modules = [module for line in player.layer.map for module in line]
    for module in modules:
        if module._func is None:
            modules.remove(module)

    for index, module in enumerate(modules, 1):
        print "%i: %s - %i" % (index, repr(module)[1:-1], module.hp)

    choice = None
    while choice is None:
        try:
            index = int(raw_input("Module number to repair: "))
        except:
            print "Invalid choice"
            continue
        if index > len(modules):
            print "Invalid choice"
            continue
        else:
            print "%s selected." % (repr(modules[index - 1]),)
            choice = (index - 1)

    modules[choice].hp += mat
    print "%s consumed" % (plate,)
    player.cargo.remove(plate)

game.new_cmd["repair"] = game.new_cmd["armor"] = game.new_cmd["reinforce"] = repair
game.cmd_list["repair"] = "use manufactured plates to reinforce your hull"
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
            values.append(random.randrange(20, 100))
            values.append(random.randrange(0, 20))
            
            material_data[mat] = values
        world.mat_data = material_data

for i in xrange(3):
    lp.blueprint_types.append("plate")

main = lp.main

if __name__ == "__main__":
    import leviathans_obc
    main()
