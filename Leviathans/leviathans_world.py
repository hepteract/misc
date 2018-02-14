#Embedded file name: leviathans_world.pyc
ENABLE_COMBAT = True
MINIMUM_SYSTEMS = 10
MAXIMUM_SYSTEMS = 100
SYSTEM_BASE = {}
SOUNDTRACK = 'below_the_asteroids.mp3'
LOOT = ('Metal Scrap', 'Metal Scrap', 'Metal Scrap', 'Officer Insignia',\
        'Top Secret Report', 'Antimatter Canister')
from leviathans import ShipLayer, ShipModule, generate_crew_roster
from progressbar import ProgressBar, AnimatedMarker
import leviathans_battle as lb
from copy import deepcopy as copy
import cPickle as pickle
import threading, random, name, time, sys, os
import logging
if __name__ != '__main__':
    logging.debug('%s imported', __name__)

try:
    import readline
    logging.debug('readline imported')
except:
    logging.warning('Unable to import readline')

cmd_list = {'map': 'Display a list of the accesible jump beacons in the system.',
 'jump (system)': "Jump to the solar system 'system', if it is in the list of accesible jump beacons.",
 'quit': 'Save and exit the game.'}

class Apotheosis(Exception):
    pass


class Death(Exception):
    pass

loop_hooks = ()
def loop_hook(hook):
    global loop_hooks
    loop_hooks += (hook,)
    return hook

battle_hooks = ()
def battle_hook(hook):
    global battle_hooks
    battle_hooks += (hook,)
    return hook

world_hooks = ()
def world_hook(hook):
    global world_hooks
    world_hooks += (hook,)
    return hook

def wrap_loop_hook(world, playerid):
    def wrapper(func):
        def main(*args):
            return func(world, playerid)
        return main
    return wrapper

def wrap_battle_hook(world, playerid):
    def wrapper(func):
        def main(*args):
            return func(world, playerid, *args)
        return main
    return wrapper

def get_help():
    logging.info('Help requested')
    print
    print 'Welcome aboard the USS Leviathan, Captain!'
    print '\n=======HELP=======\n'
    print "All commands are case-insensitive, and additional text doesn't matter. For example:"
    print '"jump Hek A" is the same as "Jump into Hek A!", which is the same as "You know that system, Hek A? Jump to it."'
    print
    if ENABLE_COMBAT == True:
        print 'In combat, you can use the following commands:'
        lb.get_help(False)
        print 'When not in combat, you can use these commands:'
    else:
        logging.warning('Space combat is currently disabled in this version of Leviathans due to technical difficulties. The outcome of combats will be randomized.')
    print
    for cmd, desc in cmd_list.items():
        print cmd, '--', desc

    print '\n=====END HELP=====\n'


item_prefix = ('Deep Space', 'Stolen', 'Deadspace', 'Officer', 'Experimental', 'Prototype', 'Advanced', 'Terran', 'Ancient', 'Secret', 'Alien', 'Quantum', 'Zero-Point', 'Antimatter', 'Faction', 'Matrix', 'Photonic', 'Nuclear')
item_body = {'movt': ('Thrusters', 'Warp Drive', 'Afterburner', 'Micro Warp Drive', 'Jump Drive', 'Micro Jump Drive', 'Drive'),
 'movr': ('RCS Thrusters', 'Maneuvering Thrusters', 'Directional Drive'),
 'hull': ('Armor Plating', 'Hull Plating', 'Armor', 'Bulkheads'),
 'dmg': ('Torpedo Launcher', 'Phaser Array', 'Laser Cannons', 'Laser Array', 'Phaser Cannons', 'Missile Rack', 'Missile Bay', 'Missile Launcher'),
 'scn': ('Sensor Array', 'Scanner Array', 'Scanning Array', 'Sensory Drones', 'Camera Drones')}
prefix_mods = {'3/27': 'Specially Named',
 '12/25': ('Holiday', 'Christmas', "Santa's"),
 '4,13': ('Unlucky', 'Cursed'),
 '4/1': ('Joke', "Fool's", 'Rick Roll', "Rick Roll'd", 'Rickroll', 'Rickrolled'),
 '4/5': ('Vulcan', 'First Contact', 'Federation'),
 '*': "str(ltime.tm_year + 900) + '-series'",
 '1/1': ("New Year's", 'Resolved'),
 '12/31': ("New Year's", 'Resolved'),
 '1/21': "Martin's",
 '2/2': "The Groundhog's",
 '2/10': 'New Chinese',
 '2/14': ('Love', 'Lovey Dovey'),
 '2/18': 'Presidential',
 '3/10': 'Daylight',
 '3/17': ('Green', 'LuckyLEPrecon', 'Leprechaun'),
 '3/20': ('Equinox', 'Spring'),
 '3/31': ('Easter', 'Birth', 'Rebirth', 'Bunny', 'Peeps'),
 '5/12': ("Mothers'", 'Motherhood', 'Mommy'),
 '5/27': 'Memorial',
 '6/14': ("Fathers'", 'Fatherhood', 'Daddy'),
 '6/21': ('Solstice', 'Summer'),
 '7/4': ('Independent', 'Independence', 'Firework'),
 '7/28': ("Parents'", 'Parenthood'),
 '9/2': ('Labor', 'Laborious'),
 '9/11': ('Patriot', 'Terrorist'),
 '9/22': ('Autumn', 'Fall', 'Equinox'),
 '10/14': ("Invader's", "Columbus's", "Go claim someone's house as your own with this"),
 '10/31': ('Terrifying', 'Scary', 'Bloody', 'Horrifying'),
 '11/3': 'Daylight',
 '11/5': ("Alexander's", 'Birthday'),
 '11/11': ("Veterans'", 'Veteran'),
 '11/28': 'Hanukkah',
 '11/28': ('Thanksgiving', 'Thank You'),
 '11/29': ('Black', 'Shopping'),
 '12/7': ('Pearl', 'Pearl Harbor', 'Remembrance'),
 '12/7': ("Ellie's", 'Birthday'),
 '12/21': ('Solstice', 'Winter'),
 '12/26': ('Kwanzaa', 'Unity', 'Umoja', 'First')}
body_mods = {}

def apply_mods():
    global item_prefix
    logging.debug('Applying prefix modifications')
    ltime = time.localtime()
    _pre = list(item_prefix)
    for date, mod in prefix_mods.items():
        if date == str(ltime.tm_mon) + '/' + str(ltime.tm_mday) or date == str(ltime.tm_mon) or date == str(ltime.tm_wday) + ',' + str(ltime.tm_mday):
            if type(mod) in (list, tuple):
                for m in mod:
                    _pre.append(m)

            else:
                _pre.append(mod)
        elif date == '*':
            if type(mod) in (list, tuple):
                _pre.append(str(eval(str(getattr(ltime, mod[0])) + mod[1])))
            else:
                _pre.append(str(eval(mod)))

    item_prefix = tuple(_pre)
    for date, modtuple in body_mods.items():
        if date == str(ltime.tm_mon) + str(ltime.tm_day) or date == str(ltime.tm_mon) or date == str(ltime.tm_wday) + ',' + str(ltime.tm_mday):
            _temp = list(item_body[modtuple[0]])
            if type(modtuple[1]) in (list, tuple):
                for mod in modtuple[1]:
                    _temp.append(mod)

            else:
                _temp.append(mod)
            item_body[modtuple[0]] = tuple(_temp)

    if '4/1' == str(ltime.tm_mon) + '/' + str(ltime.tm_mday):
        import webbrowser as wb
        print 'Welcome to Leviathans, Captain.\n'
        raw_input('Congratulations! You have unlocked an exclusive new area! Press the Enter key to explore it. ')
        wb.open('http://tinyurl.com/new-solarsystem')
        print 'Loading...'
        time.sleep(5)


apply_mods()

class ultrapass(object):

    def __getattr__(self, *args, **kwargs):
        pass


WORLD_PROTOTYPE = ultrapass()

def make_enemyship():
    pass


class System(object):

    def __init__(self, world, id = 0, name = None, jumps = [], enemy = 'rand'):
        self.ID = id
        self.name = 'J' + id if name is None else name
        self.jumpgates = []
        for jump in jumps:
            self.jumpgates.append({id: jump,
             jump: id})

        self.enemy = enemy if enemy != 'rand' else random.choice((make_enemyship(world, world.market), None))


class Item(object):

    def __init__(self, id, name, quality, func):
        self.ID = id
        self.name = name
        self.quality = quality
        self.func = func
        if func == 'movt' or func == 'movr':
            func = 'mov'
        self.self = ShipModule(self.quality * 50, func=func, mag=quality * 50, axis=-1, pos=1, type='thrust' if func == 'movt' else 'rotate')


class Ship(object):

    def __init__(self, layer = None, inv = [], system = 0, crew = None, debug = False, cargo = [], loc = None):
        self.systemID = system
        self.inv = inv
        self.crew = generate_crew_roster(len(inv) * 10 + 5) if crew is None else crew
        self.captain = self.crew[0]
        self.cargo = cargo if type(cargo) != tuple else [ cargo[0] for i in xrange(cargo[1]) ]
        self.orbit = loc
        while len(inv) < 11:
            self.inv.append(Item(-1, 'None', 0, ShipModule(func=None)))

        self.inv.reverse()
        for i, item in enumerate(self.inv, 0):
            item.self.crew = self.crew[-i * 10:-(i + 1) * 10]

        self.inv.reverse()
        if layer is None:
            self.layer = ShipLayer([[ShipModule(func='dmg', mag=100, axis=0, pos=1, crew=self.crew[95:105]), ShipModule(func='scn', crew=self.crew[85:95]), ShipModule(func='dmg', mag=100, axis=0, pos=1, crew=self.crew[105:115])],
             [ShipModule(crew=self.crew[5:15]), ShipModule(func='Bridge', symbol='@', crew=self.crew[:5]), ShipModule(crew=self.crew[25:35])],
             [ShipModule(crew=self.crew[35:45]), ShipModule(func='mov', type='thrust', mag=1, dir=1, crew=self.crew[45:55]), ShipModule(crew=self.crew[5005:65])],
             [ShipModule(func='mov', type='rotate', crew=self.crew[65:75]), ShipModule(func=None), ShipModule(func='mov', type='rotate', crew=self.crew[75:85])]])
        else:
            self.layer = layer

    def __repr__(self):
        return repr(self.layer)

    def __str__(self):
        return str(self.layer)


def make_playership(world, market, cargo = []):
    inv = []
    while len(inv) < 10:
        for id, price in market.items():
            item = world.items[id]
            if (len(inv) == 0 or len(inv) == 2) and item.func == 'dmg':
                inv.append(copy(item))
            elif len(inv) == 1 and item.func == 'scn':
                inv.append(copy(item))
            elif (len(inv) == 3 or len(inv) == 4 or len(inv) == 5 or len(inv) == 7) and item.func == 'hull':
                inv.append(copy(item))
            elif len(inv) == 6 and item.func == 'movt':
                inv.append(copy(item))
            elif (len(inv) == 8 or len(inv) == 9) and item.func == 'movr':
                inv.append(copy(item))

    return Ship(inv=inv, cargo=cargo)


def make_enemyship(world, market):
    inv = []
    while len(inv) < 10:
        for id, price in market.items():
            item = world.items[id]
            if len(inv) == 1 and item.func == 'dmg':
                inv.append(copy(item))
            elif (len(inv) == 3 or len(inv) == 4 or len(inv) == 5 or len(inv) == 7 or len(inv) == 0 or len(inv) == 2) and item.func == 'hull':
                inv.append(copy(item))
            elif len(inv) == 6 and item.func == 'movt':
                inv.append(copy(item))
            elif (len(inv) == 8 or len(inv) == 9) and item.func == 'movr':
                inv.append(copy(item))

    return Ship(inv=inv)


class GameWorld(object):

    def __init__(self, players = ['Ship()'], systems = SYSTEM_BASE, market = {}, items = {}, notify = True, start_cargo = []):
        logging.info('Generating new world')
        if notify:
            print 'Generating new world...\n\nGenerating items...'
        logging.debug('Generating items')
        self.items = self.generate_items() if items == {} else items
        if notify:
            print 'Generating market orders...'
        logging.debug('Generating market orders')
        logging.warning('The market is not yet accessible to players')
        self.market = self.generate_market() if market == {} else market
        if notify:
            print 'Generating solar systems...'
        logging.debug('Generating solar systems')
        self.systems = self.generate_systems(notify) if systems == {} else systems
        if notify:
            print 'Spawning players...'
        logging.debug('Spawning players')
        self.players = [make_playership(self, self.market, start_cargo)] if players == ['Ship()'] else players
        if notify:
            print '\nWorld generation done!\n'
        logging.info('World generation done')

    def __get_systems(self):
        slist = []
        for system in self.systems.values():
            slist.append(system)

        return slist

    system_list = property(__get_systems)

    def get_jumps(self, systemID):
        if systemID in self.systems:
            gates = []
            for gate in self.systems[systemID].jumpgates:
                gates.append(gate[systemID])

    def generate_systems(self, notify = True):
        global MINIMUM_SYSTEMS
        global MAXIMUM_SYSTEMS
        maxval = random.randrange(MINIMUM_SYSTEMS, MAXIMUM_SYSTEMS)
        if notify:
            pbar = ProgressBar()
        else:
            pbar = ultrapass()
        systems = {}
        name.seed()
        systems[0] = System(self, 0, name.generate(sep='', prefix=name.prefixes, body=name.sounds, bodies=random.randrange(1, 5), _terminate=random.choice(name.suffixes), suffix=name.postfix_func(' ', name.alphabetize)), (1, random.randrange(1, 5)))
        for i in pbar(xrange(1, maxval)):
            systems[i] = System(self, i, name.generate(sep='', prefix=name.prefixes, body=name.sounds, bodies=random.randrange(1, 5), _terminate=random.choice(name.suffixes), suffix=name.postfix_func(' ', name.alphabetize)), (i + 1, i - 1, random.randrange(0, i + 5)))
            logging.debug('Solar system generation loop at %i/%i', i, maxval)

        return systems

    def generate_items(self):
        items = {}
        name.seed()
        for i in xrange(0, random.randrange(10, 276)):
            func = random.choice(('dmg', 'scn', 'movt', 'movr', 'hull'))
            items[i] = Item(i, name.generate_legacy(sep=' ', prefix=item_prefix, body=item_body[func], suffix=name.romanize), random.randrange(0, 10) + 1, func)

        return items

    def generate_market(self):
        market = {}
        for id, item in self.items.items():
            market[id] = random.randrange(max((item.quality - 5, 1)), item.quality + 6) * 1000

        return market

    def __repr__(self):
        return '<GameWorld consisting of ' + str(len(self.systems.keys())) + (' solar system>' if len(self.systems) == 1 else ' solar systems and ') + str(len(self.players)) + (' player>' if len(self.players) == 1 else ' players>')


functions = {'movt': 'Propulsion',
 'movr': 'Rotation',
 'hull': 'Hull',
 'dmg': 'Weapon',
 'scn': 'Sensors'}

def new_world(save = True, notify = True):
    logging.debug('Generating new world')
    world = GameWorld()

    for hook in world_hooks:
        hook(True, world)
    
    worldfile = open('world.dat', 'wb')
    if save:
        if notify:
            pbar = ProgressBar(widgets=['Saving: ', AnimatedMarker()], maxval=600).start()
        savethread = threading.Thread(target=pickle.dump, args=(world, worldfile), kwargs={'protocol': pickle.HIGHEST_PROTOCOL})
        savethread.start()
        i = 0
        while savethread.isAlive():
            pbar.update(i)
            i += 1 if i != 600 else -599
            time.sleep(0.1)

    worldfile.close()
    return world


def load_world(save = True, notify = True):
    logging.debug('Loading saved world')
    worldfile = open('world.dat', 'rb')
    try:
        world = pickle.load(worldfile)
    except AttributeError:
        logging.error("Save file is corrupt or from a different version")
        print "Save file is corrupt or from a different version"
        exit()
    worldfile.close()

    for hook in world_hooks:
        hook(False, world)
        
    return world


def save_world(world, notify = True):
    logging.debug('Saving world')
    worldfile = open('world.dat', 'wb')
    if notify:
        pbar = ProgressBar(widgets=['Saving: ', AnimatedMarker()], maxval=600).start()
    savethread = threading.Thread(target=pickle.dump, args=(world, worldfile), kwargs={'protocol': pickle.HIGHEST_PROTOCOL})
    savethread.start()
    i = 0
    while savethread.isAlive():
        pbar.update(i)
        i += 1 if i != 600 else -599
        time.sleep(0.1)

    worldfile.close()


def replacement_simple_demo(*args, **kwargs):
    logging.warning('Raising AttributeError to end combat')
    raise AttributeError, 'space combat not supported in this version of Leviathans'


if not ENABLE_COMBAT:
    lb._simple_demo = replacement_simple_demo
new_cmd = {}

def _play_world(world, playerid = 0):
    player = world.players[playerid]
    print 'Welcome to', world.systems[player.systemID].name + ', Captain!\n'
    while True:
        for hook in loop_hooks:
            hook(world, playerid)
            
        cmd = raw_input("We're currently in " + world.systems[player.systemID].name + ', Captain. Your orders?\n').lower()
        logging.info("Command '%s' recieved", cmd)
        found = False
        if player.systemID >= len(world.system_list) - 1 and len(world.system_list) > 1:
            raise Apotheosis
        for _cmd in new_cmd:
            if _cmd in cmd:
                found = True
                new_cmd[_cmd](world, cmd, playerid)
                break

        if found:
            continue
        if 'jump' in cmd or 'warp' in cmd:
            jumped = None
            try:
                for jump in world.systems[player.systemID].jumpgates:
                    if world.system_list[jump[player.systemID]].name.lower() in cmd:
                        try:
                            player.systemID = world.system_list.index(world.system_list[jump[player.systemID]])
                        except KeyError:
                            print 'Jump succeeded!\n'

                        jumped = player.systemID

                if jumped != None:
                    print 'Welcome to', world.systems[player.systemID].name + ', Captain!\n'
                else:
                    print "I'm sorry, Captain. We are unable to jump to that system."
            except KeyError:
                print 'Jump succeeded!\n'

        elif 'map' in cmd:
            for jump in world.systems[player.systemID].jumpgates:
                try:
                    if jump[player.systemID] != player.systemID:
                        print world.system_list[jump[player.systemID]].name, '(Sector', str(jump[player.systemID]) + ')'
                except IndexError:
                    raise Apotheosis

        else:
            if 'ready room' in cmd or 'quit' in cmd or 'retire' in cmd:
                save_world(world)
                return
            if 'inject' in cmd:
                exec raw_input('> ')
                print
            elif 'help' in cmd:
                get_help()
                continue
            elif 'raise' in cmd:
                raise Exception, 'Raise invoked from command line'
            elif 'suicide' in cmd:
                raise Death, 'Suicide'
            elif 'module' in cmd:
                for module in sys.modules.keys():
                    if module.startswith('leviathans'):
                        print module

                print
        if world.systems[player.systemID].enemy != None:
            print '\nSir! An enemy ship is aproaching us', random.choice(('out of nowhere!', 'from behind a planet!', 'after leaving a station!', 'with its guns loaded!')), '\n'

            wrapper = wrap_loop_hook(world, playerid)
            wrap = wrap_battle_hook(world, playerid)
            lb.loop_hooks = tuple([wrapper(func) for func in loop_hooks])
            lb.loop_hooks += tuple([wrap(func) for func in battle_hooks])
            
            ship = lb.main(False, ship0=player.layer, player_crew=player.crew, diff=player.systemID)
            if ship == False:
                raise Death
            else:
                player.cargo.append(random.choice(LOOT))
                world.systems[player.systemID].enemy = None
                player.layer = ship
                print


def play_world(world, playerid = 0):
    try:
        _play_world(world, playerid)
    except KeyboardInterrupt:
        print '^C recieved.'
        logging.info('^C recieved')
        if not raw_input('Save (y/n)? ') == 'n':
            save_world(world)
    except Death:
        print '\nSorry, you died.\n'
        logging.info('Player dead')
        world.players.pop(playerid)
        if playerid < len(world.players):
            if raw_input("Activate clone (y/n)? ").lower() != "n":
                print 'Clone activated.\n'
                logging.info('Clone activated')
                play_world(world, playerid)
        cmd = None
        while cmd != '':
            cmd = raw_input('Press the [Enter] key to exit> ')
            exec cmd
    except Apotheosis:
        print '\nCongratulations! You and you crew have achieved apotheosis.'
        logging.info('Player achieved enlightenment')
        cmd = None
        while cmd != '':
            cmd = raw_input('\nPress the [Enter] key to exit> ')
            exec cmd
    except Exception as e:
        print 'Uh oh. It appears that Leviathans has crashed (' + str(e) + ').'
        logging.critical('%s : %s', sys.exc_info()[0].__name__, sys.exc_info()[1])
        if not raw_input('Save (only save if debugging -- otherwise, make a new world) (y/n)? ') == 'n':
            save_world(world)
        cmd = None
        while cmd != '':
            cmd = raw_input('\nPress the [Enter] key to exit> ')
            logging.info("Command '%s' recieved in exit menu")
            exec cmd

        logging.exception('Exception recieved in leviathans_world')
        raise


start_new = lambda save = input: play_world(new_world(save if save != input else not raw_input('Save after creation (y/n)? ') == 'n'))
resume = lambda : play_world(load_world())
_main = lambda new = False: (resume if new else start_new)()

def worldgen():
    world = GameWorld()
    print 'Items in world:'
    for id, item in world.items.items():
        print id, ':', item.name, '(Quality', item.quality, functions[item.func] + ')', '-', world.market[id], 'credits'

    print '\nSystems:'
    for id, system in world.systems.items():
        print system.name


def main():
    new = raw_input('Create new world (y/n)? ') == 'n'
    _main(new)


def quickgen(module = None):
    if module is None:
        global MINIMUM_SYSTEMS
        global MAXIMUM_SYSTEMS
        MINIMUM_SYSTEMS = 10
        MAXIMUM_SYSTEMS = 100
    else:
        module.MINIMUM_SYSTEMS = 10
        module.MAXIMUM_SYSTEMS = 100      


def jovian(module = None):
    if module is None:
        global MINIMUM_SYSTEMS
        global MAXIMUM_SYSTEMS
        MINIMUM_SYSTEMS = 5
        MAXIMUM_SYSTEMS = 10
    else:
        module.MINIMUM_SYSTEMS = 5
        module.MAXIMUM_SYSTEMS = 10


def blackhole(module = None):
    if module is None:
        global EVAL_SYSTEM_BASE
        EVAL_SYSTEM_BASE = '{0 : System(game.WORLD_PROTOTYPE, 0, name.generate(sep = "", prefix = name.prefixes, body = name.sounds, bodies = random.randrange(1, 5), _terminate = random.choice(name.suffixes), suffix = name.postfix_func(" ", name.alphabetize)), (), enemy = None)}'
    else:
        module.EVAL_SYSTEM_BASE = '{0 : System(game.WORLD_PROTOTYPE, 0, name.generate(sep = "", prefix = name.prefixes, body = name.sounds, bodies = random.randrange(1, 5), _terminate = random.choice(name.suffixes), suffix = name.postfix_func(" ", name.alphabetize)), (), enemy = None)}'

if __name__ == '__main__':
    jovian()
    main()
