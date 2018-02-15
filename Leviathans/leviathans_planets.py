#!/usr/bin/python
#Embedded file name: leviathans_planets.pyc
from leviathans_world import System, worldgen
from nova.hook import HookTarget
from name import int_to_roman, name, romanize, seed, element_name
import collections
import random, pickle
import progressbar
import threading
import time
import save as save_form
import sys
import logging
import leviathans_world as game
game.EVAL_SYSTEM_BASE = '{}'
if __name__ != '__main__':
    logging.debug('%s imported', __name__)
game.cmd_list['prospect'] = 'Scan all the planets in the solar system for resources.'
game.cmd_list['mine (planet)'] = "Mine the planet 'planet'."
game.cmd_list['cargo'] = 'Display the contents of your cargo hold.'
game.cmd_list['get trades [planet]'] = "Get a list of the currently available trades in the central space station in the solar system, or on planet 'planet'"
game.cmd_list['sell (item) [planet]'] = "Sell the item 'item' to the central space station, or to the planet 'planet'"
game.cmd_list['research'] = 'Research a new item'
game.cmd_list['manufacture (blueprint)'] = "Manufacture an item according to the blueprint 'blueprint'"
game.cmd_list['eat (item)'] = "Attempt to eat the item 'item'"
game.cmd_list['orbit (planet)'] = "Enter orbit around 'planet' or leave orbit"
game.cmd_list['refuel [item]'] = "Generate electroplasma from fuel"
game.cmd_list['battery'] = "Check current charge value"
game.cmd_list['status'] = "List modules and their health values"

def generate_materials(num = -1):
    logging.debug('Generating materials')
    seed()
    mat = {}
    num = num if num != -1 else random.randrange(7, 51)
    for i in xrange(num):
        #_mat = name(2) + random.choice(('nite', 'inite', 'ium', 'tine'))
        _mat = element_name()
        mat[_mat] = _mat + ' ' + random.choice(('block', 'lump', 'ingot', 'bar', 'gas container', 'liquid container', 'crystal', 'gem', 'jewel', 'stone'))

    return mat


class Planet(object):

    def __init__(self, world, name, mat = 'rand', dep = -1):
        self.world = world
        self.name = name
        self.mat = mat if mat != 'rand' else random.choice(materials.keys())
        self.dep = dep if dep != -1 else random.randrange(1, 10)

    def mine(self):
        logging.info('Mining %s', self.name)
        if self.dep > 0:
            self.dep -= 1
            return self.world.mat[self.mat]


class System(System):

    def __init__(self, world, id = 0, name = None, jumps = [], enemy = 'rand', planets = None):
        super(System, self).__init__(world, id, name, jumps, enemy)
        self.world = world
        self.planets = planets if planets is not None else self.generate_planets()
        self.dist = random.randrange(1, 10)

    def generate_planets(self):
        self.planets = []
        for i in xrange(random.randrange(0, 11)):
            self.planets.append(Planet(self.world, self.name + ' ' + int_to_roman(i + 1)))

        return self.planets

    def __enter__(self):
        logging.error("Raw System() accessed")

    def __exit__(self):
        logging.error("Raw System() accessed")        


game.System = System

"""
def find_fuel(mat):
    for item in mat.values():
        if 'fuel' in item.lower():
            return item

    mat['Petroleum'] = 'Petroleum fuel canister'
    return mat['Petroleum']
"""
# use electroplasma instead of raw fuel

def find_fuel(mat):
    return ""

standing_offers = {}
blueprints = {'Meal': 'Recipe'}

class empty(str):
    def __getitem__(self, index):
        return self

def new_world(save = True, notify = True):
    global standing_offers
    global blueprints
    global materials
    logging.debug('Generating new world')
    materials = generate_materials()
    #game.LOOT += (random.choice(materials.values()), random.choice(materials.values()), random.choice(materials.values()))
    import name
    game.SYSTEM_BASE = eval(game.EVAL_SYSTEM_BASE)
    logging.debug(game.EVAL_SYSTEM_BASE)
    name = name.name
    world = game.GameWorld(start_cargo=(find_fuel(materials), random.randrange(100, 200)), systems=game.SYSTEM_BASE)
    world.mat = materials
    world.blu = blueprints
    world.ofr = standing_offers

    #world.systems[-1] = System(world, -1, "Polaris", [0, len(world.system_list) - 2], None, [])
    #world.ofr["Polaris"] = {empty() : 'Antimatter Canister'}

    for i in xrange(5):
        item_adj = random.choice(blueprint_adj)
        item = ('' if not item_adj else item_adj + ' ') + random.choice(world.mat.keys()) + ' ' + random.choice(blueprint_types)
        item_blueprint = item + ' ' + random.choice(('Blueprint', 'Schematic', 'Template'))
        world.blu[item] = item_blueprint

    game.world_hook.run(True, world)
    
    if save:
        worldfile = open('world.dat', 'wb')
        if notify:
            pbar = progressbar.ProgressBar(widgets=['Saving: ', progressbar.AnimatedMarker()], maxval=600).start()
        savethread = threading.Thread(target=pickle.dump, args=(world, worldfile), kwargs={'protocol': pickle.HIGHEST_PROTOCOL})
        savethread.start()
        i = 0
        while savethread.isAlive():
            pbar.update(i)
            i += 1 if i != 600 else -599
            time.sleep(0.1)
        worldfile.close()
    
    return world

game.new_world = new_world

def load_world(save = True, notify = True):
    global standing_offers
    global blueprints
    global materials
    logging.debug('Loading saved world')
    worldfile = open('world.dat', 'rb')
    try:
        world = pickle.load(worldfile)
    except:
        logging.error("Save file is corrupt or from a different version")
        print "Save file is corrupt or from a different version"
        exit()
    worldfile.close()
    blueprints = world.blu
    materials = world.mat
    standing_offers = world.ofr
    game.LOOT += (random.choice(materials.values()), random.choice(materials.values()), random.choice(materials.values()))

    game.world_hook.run(False, world)
    
    return world


game.load_world = load_world

scan_hook = HookTarget()

def prospect(world, cmd, playerid):
    if cmd: logging.info('Prospecting solar system for planetary resources')
    else: logging.debug('Prospecting solar system for planetary resources') 
    
    materials = world.mat
    player_system = world.system_list[world.players[playerid].systemID]
    if len(player_system.planets):
        for planet in player_system.planets:
            out = [planet.name, ':', planet.mat]
            if planet.dep <= 0:
                out.append('(depleted)')
            if world.players[playerid].orbit == planet.name:
                out.append('(orbiting)')
            print " ".join(out)

    else:
        print 'Sorry, there are no planets in this solar system.'

    print

    scan_hook.run(world, playerid)


game.new_cmd["scan"] = game.new_cmd['prospect'] = prospect

def status(world, cmd, playerid):
    player = world.players[playerid]

    modules = [module for line in player.layer.map for module in line]
    for module in modules:
        if module._func is None:
            modules.remove(module)

    for index, module in enumerate(modules, 1):
        print "%i: %s - %i" % (index, repr(module)[1:-1], module.hp)

game.new_cmd['status'] = game.new_cmd['modules'] = status

def mine(world, cmd, playerid):
    player_system = world.system_list[world.players[playerid].systemID]
    player_system.planets.reverse()
    for planet in player_system.planets:
        if planet.name.lower() in cmd:
            logging.info('Mining planet %s for %s', planet.name, planet.mat)
            print 'Mining lasers activated.'
            print
            print 'The following has been added to your cargo bay:'
            mined = planet.mine()
            if mined != None:
                world.players[playerid].cargo.append(mined)
                print mined
            else:
                print 'Nothing (' + planet.name, 'has been completely depleted of', planet.mat + ')'
            print
            player_system.planets.reverse()
            return mined
    for planet in player_system.planets:
        if world.players[playerid].orbit == planet.name:
            logging.info('Mining planet %s for %s', planet.name, planet.mat)
            print 'Mining lasers activated.'
            print
            print 'The following has been added to your cargo bay:'
            mined = planet.mine()
            if mined != None:
                world.players[playerid].cargo.append(mined)
                print mined
            else:
                print 'Nothing (' + planet.name, 'has been completely depleted of', planet.mat + ')'
            print
            player_system.planets.reverse()
            return mined
    print "I'm sorry, Captain, but we cannot currently mine that planet.\n"
    player_system.planets.reverse()

game.new_cmd['mine'] = mine

def orbit(world, cmd, playerid):
    player_system = world.system_list[world.players[playerid].systemID]
    player_system.planets.reverse()
    for planet in player_system.planets:
        if planet.name.lower() in cmd:
            logging.info('Entering orbit of %s', planet.name)
            print "Entering orbit of %s" % (planet.name,)
            world.players[playerid].orbit = planet.name
            print
            player_system.planets.reverse()
            return planet.name
    if "leave" in cmd:
        logging.info('Leaving orbit')
        print "Leaving orbit"
        world.players[playerid].orbit = None
    else:
        print "I'm sorry, Captain, but we cannot currently orbit that planet.\n"
    player_system.planets.reverse()

game.new_cmd['orbit'] = orbit
            
def cargo(world, cmd, playerid):
    if cmd: logging.info('Checking contents of cargo hold')
    else: logging.debug('Checking contents of cargo hold')
    quantities = {}
    for item in world.players[playerid].cargo:
        if item in quantities:
            quantities[item] += 1
        else:
            quantities[item] = 1
    quantities = collections.OrderedDict(sorted(quantities.items()))

    if "" in quantities:
        del quantities[""]

    for item, quantity in quantities.iteritems():
        print quantity, item + ('' if quantity == 1 else 's')

    if quantities == {}:
        print 'Your cargo hold is empty.'
    print

game.new_cmd['cargo'] = cargo

def battery(world, cmd, playerid):
    if cmd: logging.info("Checking charge of battery")
    else: logging.debug("Checking charge of battery")

    charge = world.players[playerid].cargo.count("")

    print charge, "hyperjoule" if charge == 1 else "hyperjoules", "of charge available"
    print

game.new_cmd['battery'] = game.new_cmd['charge'] = game.new_cmd["plasma"] = battery

blueprint_adj = list(game.item_prefix) + [ None for i in xrange(50) ]
blueprint_types = ['toy',
 'coin',
 'brick',
 'pole',
 'container',
 'tube',
 'pipe',
 'cube',
 'computer',
 'plate',
 'fuel container']

def research(world, cmd, playerid):
    logging.info('Researching')
    item_adj = random.choice(blueprint_adj)
    item = ('' if not item_adj else item_adj + ' ') + random.choice(world.mat.keys()) + ' ' + random.choice(blueprint_types)
    item_blueprint = item + ' ' + random.choice(('Blueprint', 'Schematic', 'Template'))
    blueprints[item] = item_blueprint
    print 'The following has been added to your cargo bay:'
    logging.info('Adding %s to player cargo bay', item_blueprint)
    world.players[playerid].cargo.append(item_blueprint)
    print item_blueprint


game.new_cmd['research'] = research

def manufacture(world, cmd, playerid):
    for blueprint in blueprints:
        if blueprint.lower() in cmd:
            for item in world.players[playerid].cargo:
                if item in world.mat.values():
                    if world.mat.keys()[world.mat.values().index(item)] in blueprint:
                        print 'Manufacturing', 'an' if blueprint[0].lower() in 'aeiou' else 'a', blueprint + '...'
                        logging.info('Manufacturing accroding to %s', blueprints[blueprint])
                        world.players[playerid].cargo.append(blueprint)
                        world.players[playerid].cargo.remove(item)
                        return

    print "I'm sorry, Captain. We are currently unable to manufacture that item."


game.new_cmd['manufacture'] = manufacture

def get_trades(world, cmd, playerid):
    logging.info('Getting trade data')
    player_system = world.system_list[world.players[playerid].systemID]
    player_system.planets.reverse()
    for planet in player_system.planets:
        if planet.name.lower() in cmd:
            print 'Contacting', planet.name, 'via orbital relays...'
            print 'Establishing communication with planetary trade hub...'
            print
            if planet.name not in standing_offers:
                standing_offers[planet.name] = {}
                for i in xrange(random.randrange(1, 10)):
                    standing_offers[planet.name][random.choice(random.choice((blueprints.keys(), materials.values())))] = random.choice(random.choice((blueprints.keys(), materials.values())))

            for buy, sell in standing_offers[planet.name].items():
                print 'OFFER:', 'An' if sell[0].lower() in 'aeiou' else 'A', sell, 'for', 'an' if buy[0].lower() in 'aeiou' else 'a', buy

            player_system.planets.reverse()
            return
        
    for planet in player_system.planets:
        if planet.name == world.players[playerid].orbit:
            print 'Contacting', planet.name, 'via orbital relays...'
            print 'Establishing communication with planetary trade hub...'
            print
            if planet.name not in standing_offers:
                standing_offers[planet.name] = {}
                for i in xrange(random.randrange(1, 10)):
                    standing_offers[planet.name][random.choice(random.choice((blueprints.keys(), materials.values())))] = random.choice(random.choice((blueprints.keys(), materials.values())))

            for buy, sell in standing_offers[planet.name].items():
                print 'OFFER:', 'An' if sell[0].lower() in 'aeiou' else 'A', sell, 'for', 'an' if buy[0].lower() in 'aeiou' else 'a', buy

            player_system.planets.reverse()
            return

    print 'Contacting central space station in', player_system.name + '...'
    print 'Establishing communication with station marketplace...'
    print
    if player_system.name not in standing_offers:
        standing_offers[player_system.name] = {}
        for i in xrange(random.randrange(1, 10)):
            standing_offers[player_system.name][random.choice(random.choice((blueprints.keys(), materials.values())))] = random.choice(random.choice((blueprints.keys(), materials.values())))

    for buy, sell in standing_offers[player_system.name].items():
        print 'OFFER:', 'An' if sell[0].lower() in 'aeiou' else 'A', sell, 'for', 'an' if buy[0].lower() in 'aeiou' else 'a', buy

    player_system.planets.reverse()


game.new_cmd['get trade'] = get_trades

def trade(world, cmd, playerid):
    logging.info('Executing trade')
    player_system = world.system_list[world.players[playerid].systemID]
    player_system.planets.reverse()
    for planet in player_system.planets:
        if planet.name.lower() in cmd:
            print 'Contacting', planet.name, 'via orbital relays...'
            print 'Establishing communication with planetary trade hub...'
            print
            if planet.name not in standing_offers:
                standing_offers[planet.name] = {}
                for i in xrange(random.randrange(1, 10)):
                    standing_offers[planet.name][random.choice(random.choice((blueprints.keys(), materials.keys())))] = random.choice(random.choice((blueprints.keys(), materials.keys())))

            for buy, sell in standing_offers[planet.name].items():
                logging.debug('Testing for %s in %s', buy, cmd)
                if buy.lower() in cmd:
                    if buy in world.players[playerid].cargo:
                        logging.debug('True')
                        world.players[playerid].cargo.remove(buy)
                        world.players[playerid].cargo.append(sell)
                        print 'Bought', 'an' if sell[0].lower() in 'aeiou' else 'a', sell, 'for', 'an' if buy[0].lower() in 'aeiou' else 'a', buy
                        logging.info('%s traded for %s', buy, sell)
                        player_system.planets.reverse()
                        return
                    else:
                        print 'Sorry, you cannot fill that order due to a lack of the included items.'
                        logging.info('Player attempted to trade %s for %s, but was missing the required item (%s)', buy, sell, buy)
                        player_system.planets.reverse()
                        return
                else:
                    logging.debug('False')

            print 'Sorry, the trade hub on that planet has no standing offers for that item.'
            logging.warning('Invalid item for planetary trade')
            player_system.planets.reverse()
            return
    for planet in player_system.planets:
        if planet.name == world.players[playerid].orbit:
            print 'Contacting', planet.name, 'via orbital relays...'
            print 'Establishing communication with planetary trade hub...'
            print
            if planet.name not in standing_offers:
                standing_offers[planet.name] = {}
                for i in xrange(random.randrange(1, 10)):
                    standing_offers[planet.name][random.choice(random.choice((blueprints.keys(), materials.keys())))] = random.choice(random.choice((blueprints.keys(), materials.keys())))

            for buy, sell in standing_offers[planet.name].items():
                logging.debug('Testing for %s in %s', buy, cmd)
                if buy.lower() in cmd:
                    if buy in world.players[playerid].cargo:
                        logging.debug('True')
                        world.players[playerid].cargo.remove(buy)
                        world.players[playerid].cargo.append(sell)
                        print 'Bought', 'an' if sell[0].lower() in 'aeiou' else 'a', sell, 'for', 'an' if buy[0].lower() in 'aeiou' else 'a', buy
                        logging.info('%s traded for %s', buy, sell)
                        player_system.planets.reverse()
                        return
                    else:
                        print 'Sorry, you cannot fill that order due to a lack of the included items.'
                        logging.info('Player attempted to trade %s for %s, but was missing the required item (%s)', buy, sell, buy)
                        player_system.planets.reverse()
                        return
                else:
                    logging.debug('False')

            print 'Sorry, the trade hub on that planet has no standing offers for that item.'
            logging.warning('Invalid item for planetary trade')
            player_system.planets.reverse()
            return

    print 'Contacting central space station in', player_system.name + '...'
    print 'Establishing communication with station marketplace...'
    print
    if player_system.name not in standing_offers:
        standing_offers[player_system.name] = {}
        for i in xrange(random.randrange(1, 10)):
            standing_offers[player_system.name][random.choice(random.choice((blueprints.keys(), materials.keys())))] = random.choice(random.choice((blueprints.keys(), materials.keys())))

    for buy, sell in standing_offers[player_system.name].items():
        logging.debug('Testing for %s in %s', buy, cmd)
        if buy.lower() in cmd:
            if buy in world.players[playerid].cargo:
                logging.debug('True')
                world.players[playerid].cargo.remove(buy)
                world.players[playerid].cargo.append(sell)
                print 'Bought', 'an' if sell[0].lower() in 'aeiou' else 'a', sell, 'for', 'an' if buy[0].lower() in 'aeiou' else 'a', buy
                logging.info('%s traded for %s', buy, sell)
                player_system.planets.reverse()
                return
            else:
                print 'Sorry, you cannot fill that order due to a lack of the included items.'
                logging.info('Player attempted to trade %s for %s, but was missing the required item (%s)', buy, sell, buy)
                player_system.planets.reverse()
                return
        else:
            logging.debug('False')

    print 'Sorry, the station in this solar system has no standing offers for that item.'
    logging.warning('Invalid item for system-wide trade')
    player_system.planets.reverse()


game.new_cmd['sell'] = trade

def eat(world, cmd, playerid):
    for item in world.players[playerid].cargo:
        if item.lower() in cmd:
            if 'meal' in item.lower():
                print 'That', item, 'was delicious!\n'
                world.players[playerid].cargo.remove(item)
                return
            else:
                print 'You tried to eat a', item, 'but it was disgusting, so you gave up.\n'
                return

    print "You don't know what to eat.\n"

game.new_cmd['eat'] = eat

def fueled_jump(world, cmd, playerid):
    player = world.players[playerid]

    fuel = ""

    if player.cargo.count(fuel) < 5:
        print "I'm sorry, Captain, but we need 10 hyperjoules to jump."
        return
    jumped = None
    try:
        for jump in world.systems[player.systemID].jumpgates:
            if world.system_list[jump[player.systemID]].name.lower() in cmd:
                try:
                    player.systemID = world.system_list.index(world.system_list[jump[player.systemID]])
                except KeyError:
                    print 'Jump succeeded!\n'

                for i in xrange(10):
                    player.cargo.remove(fuel)
                jumped = player.systemID

        if jumped != None:
            print 'Welcome to', world.systems[player.systemID].name + ', Captain!\n'
        else:
            print "I'm sorry, Captain. We are unable to jump to that system."
            print
    except KeyError:
        print 'Jump succeeded!\n'


game.new_cmd['jump'] = fueled_jump

def refuel(world, cmd, playerid):
    player = world.players[playerid]

    for item in player.cargo:
        if "fuel" in item.lower() and item.lower() in cmd and item not in blueprints.values():
            logging.info("Refueliing using %s", item)
            print "Refueling using", item

            player.cargo.remove(item)
            for i in xrange(10):
                player.cargo.append("")
            return
        elif item == "Antimatter Canister" and item.lower() in cmd:
            logging.info("Refueliing using %s", item)
            print "Refueling using", item

            player.cargo.remove(item)
            for i in xrange(40):
                player.cargo.append("")
                
            return

    for item in player.cargo:
        if "fuel" in item.lower() and item not in blueprints.values():
            logging.info("Refueliing using %s", item)
            print "Refueling using", item

            player.cargo.remove(item)
            for i in xrange(10):
                player.cargo.append("")
            return
        elif item == "Antimatter Canister":
            logging.info("Refueliing using %s", item)
            print "Refueling using", item

            player.cargo.remove(item)
            for i in xrange(40):
                player.cargo.append("")
                
            return

    logging.info("No fuel to burn")
    print "I'm sorry, sir, but we don't have any fuel to burn."

game.new_cmd['refuel'] = game.new_cmd["burn"] = refuel

def warp(world, cmd, playerid):
    player = world.players[playerid]
    jumped = None
    try:
        for jump in world.systems[player.systemID].jumpgates:
            if world.system_list[jump[player.systemID]].name.lower() in cmd:
                dist = world.system_list[jump[player.systemID]].dist
                print 'Remaining distance:'
                for i in xrange(dist):
                    sys.stdout.write(str(dist) + ' light years\r')
                    sys.stdout.flush()
                    time.sleep(10)
                    dist -= 1

                sys.stdout.write('0 light years')
                print '\n'
                try:
                    player.systemID = world.system_list.index(world.system_list[jump[player.systemID]])
                except KeyError:
                    print 'Warp succeeded!\n'

                jumped = player.systemID

        if jumped != None:
            print 'Welcome to', world.systems[player.systemID].name + ', Captain!\n'
        else:
            print "I'm sorry, Captain. We are unable to warp to that system."
    except KeyError:
        print 'Warp succeeded!\n'

game.new_cmd['warp'] = warp

@game.loop_hook
def update_cargo(world, playerid):
    with open("cargo", "w") as f:
        _stdout = sys.stdout
        sys.stdout = f
        battery(world, "", playerid)
        print "Cargo:"
        cargo(world, "", playerid)
        sys.stdout = _stdout

@game.loop_hook
def update_planets(world, playerid):
    with open("planets", "w") as f:
        _stdout = sys.stdout
        sys.stdout = f
        prospect(world, "", playerid)
        sys.stdout = _stdout

@game.battle_hook
def fire_with_fuel(world, playerid, cmd, ship0, ship1):
    if "fire" in cmd.lower():
        if "" in world.players[playerid].cargo:
            world.players[playerid].cargo.remove("")
        else:
            return -1
    return 1

main = game.main
play_world = game.play_world

if __name__ == '__main__':
    main()
