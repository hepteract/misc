#Embedded file name: leviathans_battle.pyc
from leviathans import *
from threading import Thread
import logging
if __name__ != '__main__':
    logging.debug('%s imported', __name__)

def get_help(warning = True):
    logging.warning('Help feature not yet implemented')
    
    if warning:
        print '(help feature not yet implemented (ask Elijah) )'


def boarding_parties():
    print 'Sending boarding parties...'
    boarding_party = CrewRoster([player_crew.get_random_crewmember(),
     player_crew.get_random_crewmember(),
     player_crew.get_random_crewmember(),
     player_crew.get_random_crewmember(),
     player_crew.get_random_crewmember(),
     player_crew.get_random_crewmember(),
     player_crew.get_random_crewmember(),
     player_crew.get_random_crewmember(),
     player_crew.get_random_crewmember(),
     player_crew.get_random_crewmember()])
    ship1.board(boarding_party, out=open('pipe', 'w'))
    crew_alive = 0
    for boarder in boarding_party:
        if boarder.alive:
            crew_alive += 1

    if crew_alive and crew_alive < len(boarding_party):
        print crew_alive, 'out of', len(boarding_party), "crewmembers have returned from their boarding mission, having sabotaged one of the enemy's systems."
        logging.info("%i out of %i crewmembers have returned from their boarding mission, having sabotaged one of the enemy's systems", crew_alive, len(boarding_party))
    elif crew_alive:
        print "Your boarding party returns, having sabotaged one of the enemy's systems."
        logging.info("The boarding party returns, having sabotaged one of the enemy's systems")
    else:
        print "Your boarding party failed to sabotage one of the enemy's systems, and they all died trying."
        logging.info("Your boarding party failed to sabotage one of the enemy's systems, and they all died trying")

loop_hooks = ()

def loop_hook(func):
    global loop_hooks

    loop_hooks += (func,)

def _simple_demo(captain = True, ship0 = None, player_crew = None, ship1 = None, ship1_crew = None, diff = 0):
    if captain == True:
        captain_name = raw_input('What is your name? ')
        print 'Welcome, Captain', captain_name + '!'
    elif type(captain) in (str, CrewMember):
        captain_name = str(captain)
    if player_crew == None:
        player_crew = generate_crew_roster(115, captain=captain_name)
    captain = player_crew[0]
    if ship0 == None:
        ship0 = ShipLayer([[ShipModule(func='dmg', mag=100, axis=0, pos=1, crew=player_crew[95:105]), ShipModule(func='scn', crew=player_crew[85:95]), ShipModule(func='dmg', mag=100, axis=0, pos=1, crew=player_crew[105:115])],
         [ShipModule(crew=player_crew[5:15]), ShipModule(func='Bridge', symbol='@', crew=player_crew[:5]), ShipModule(crew=player_crew[25:35])],
         [ShipModule(crew=player_crew[35:45]), ShipModule(func='mov', type='thrust', mag=1, dir=1, crew=player_crew[45:55]), ShipModule(crew=player_crew[5005:65])],
         [ShipModule(func='mov', type='rotate', crew=player_crew[65:75]), ShipModule(func=None), ShipModule(func='mov', type='rotate', crew=player_crew[75:85])]])
    if ship1_crew == None:
        ship1_crew = generate_crew_roster(85)
    if ship1 == None:
        ship1 = ShipLayer([[ShipModule(), ShipModule(func='dmg', mag=100, axis=0, pos=1, crew=ship1_crew[15:25]), ShipModule()],
         [ShipModule(crew=ship1_crew[5:15]), ShipModule(func='Bridge', symbol='@', crew=ship1_crew[:5]), ShipModule(crew=ship1_crew[25:35])],
         [ShipModule(crew=ship1_crew[35:45]), ShipModule(func='mov', type='thrust', mag=1, dir=1, crew=ship1_crew[45:55]), ShipModule(crew=ship1_crew[55:65])],
         [ShipModule(func='mov', type='rotate', crew=ship1_crew[65:75]), ShipModule(func=None), ShipModule(func='mov', type='rotate', crew=ship1_crew[75:85])]], ship_x=random.randrange(-1, 2), ship_y=random.randrange(-1, 2))
    while captain.alive:        
        print 'Your orders, Captain?'
        cmd = raw_input().lower()

        cont = True
        for hook in loop_hooks:
            if hook(cmd, ship0, ship1) == -1:
                cont = False
        if cont is False:
            continue
            
        if 'fire' in cmd or 'kill' in cmd or 'blow' in cmd or 'shoot' in cmd:
            for y in ship0.map:
                for module in y:
                    if module.func == 'dmg' and module.hp > 0:
                        print 'Firing...'

            ship0.attack(ship1)
        elif 'hail' in cmd:
            print 'They refuse all communication.'
        elif 'accelerate' in cmd:
            print 'Accelerating...'
            ship0.map[2][1].data['dir'] = 1
            ship0.map[2][1].activate(None)
        elif 'decelerate' in cmd:
            print 'Decelerating...'
            ship0.map[2][1].data['dir'] = -1
            ship0.map[2][1].activate(None)
        elif 'rotate' in cmd or 'turn' in cmd:
            print 'Rotating 90 degrees...'
            ship0.map[3][0].activate(None)
        elif 'casualty' in cmd or 'casualties' in cmd:
            for human in player_crew:
                if not human.alive:
                    print human

        elif 'enemy' in cmd:
            scanned = False
            for y in ship0.map:
                for module in y:
                    if module.func == 'scn' and not scanned:
                        scanned = True
                        print module.activate(ship1)

            if not scanned:
                print 'Sorry, you do not have a sensor array equipped.'
        elif 'status' in cmd:
            print ship0
        elif 'get our' in cmd or 'what is our' in cmd:
            print getattr(ship0, cmd.split()[2])
        elif 'get their' in cmd or 'what is their' in cmd:
            print getattr(ship1, cmd.split()[2])
        else:
            if 'retire' in cmd or 'ready room' in cmd or 'end program' in cmd or 'stop program' in cmd or 'terminate program' in cmd or 'exit program' in cmd or 'end simulation' in cmd or 'stop simulation' in cmd or 'terminate simulation' in cmd or 'exit simulation' in cmd:
                return False
            if 'repair' in cmd:
                print "Sorry, you can't repair during combat."
            else:
                if 'we surrender' in cmd:
                    print 'Your crew surrenders to the aliens, and they are allowed to live. However, they are doomed to a life of enslavement.'
                    return False
                if 'board' in cmd or 'boarding' in cmd:
                    battle_thread = Thread(target=boarding_parties)
                    battle_thread.start()
                elif 'help' in cmd:
                    get_help()
                    continue
                elif 'self' in cmd and 'destruct' in cmd:
                    for p in player_crew:
                        p.alive = False

                elif 'inject' in cmd:
                    exec raw_input('> ')
                    print
                    continue
                elif 'debug' in cmd:
                    while True:
                        exec raw_input('> ')

                    print
                    continue
                else:
                    print "I'm sorry, Captain. I don't understand what you mean."
                    logging.error("Invalid command '%s'", cmd)
                    continue
        logging.info("Command '%s' executed succesfully", cmd)
        if random.randrange(0, 100) > 50:
            logging.debug('Enemy ship attempting to fire')
            for y in ship1.map:
                for module in y:
                    if module.func == 'dmg' and module.hp > 0 and ship0.x + ship1.x in (-1, 0, 1):
                        print "Sir, we've taken a hit!"
                        logging.info('Enemy ship firing')
                        module.activate(ship0)

        destroyed = True
        for y in ship1.map:
            for module in y:
                if module.func:
                    destroyed = False

        if destroyed:
            print '\nYou defeated them!'
            logging.info('Enemy dead')
            return ship0
        print

    logging.info('Player dead')
    print 'Sorry, you died.'
    print '\nCasualties:'
    print player_crew

    return False


def generate_outcome():
    vocab = {'Part0': ['boson',
               'flux',
               'impulse',
               'neutron',
               'particle',
               'particle isotope',
               'photon',
               'plasma',
               'power',
               'proton',
               'resonance',
               'tachyon'],
     'Part1': ['control system',
               'drive',
               'drive core',
               'field',
               'jump drive',
               'hyperdrive',
               'hyperspace',
               'maintenance assembly',
               'warp field'],
     'Part2': ['accelerator',
               'array',
               'buffer',
               'capacitor',
               'compensator',
               'conduit',
               'crystal',
               'curcuit',
               'decoupling',
               'emitter',
               'generator',
               'modulator',
               'module',
               'plate',
               'reactor',
               'regulator',
               'relay',
               'rerouter'],
     'Adj1': ['backup',
              'main',
              'primary',
              'secondary',
              'tertiary',
              'front',
              'larboard',
              'lower',
              'port',
              'rear',
              'starboard',
              'upper'],
     'Adj2': ['energy',
              'gravetic',
              'ionic',
              'photonic',
              'sonic',
              'temporal'],
     'VerbPT': ['destabilized',
                'exploded',
                'imploded',
                'malfunctioned',
                'overloaded',
                'short circuited'],
     'Causing': ['causing', 'resulting in'],
     'VerbNow': ['a chain reaction',
                 'an explosion',
                 'an implosion',
                 'system failure',
                 'total shutdown']}
    gadget = ["random.choice(vocab['Part1']) + ' ' + random.choice(vocab['Part2'])",
     "random.choice(vocab['Adj1']) + ' ' + random.choice(vocab['Part0']) + ' ' + random.choice(vocab['Part1']) + ' ' + random.choice(vocab['Part2'])",
     "random.choice(vocab['Adj1']) + ' ' + random.choice(vocab['Part0']) + ' ' + random.choice(vocab['Part1'])",
     "random.choice(vocab['Adj1']) + ' ' + random.choice(vocab['Part1']) + ' ' + random.choice(vocab['Part2'])",
     "random.choice(vocab['Adj1']) + ' ' + random.choice(vocab['Part0']) + ' ' + random.choice(vocab['Part2'])",
     "random.choice(vocab['Adj2']) + ' ' + random.choice(vocab['Part0']) + ' ' + random.choice(vocab['Part1']) + ' ' + random.choice(vocab['Part2'])",
     "random.choice(vocab['Adj2']) + ' ' + random.choice(vocab['Part0']) + ' ' + random.choice(vocab['Part1'])",
     "random.choice(vocab['Adj2']) + ' ' + random.choice(vocab['Part1']) + ' ' + random.choice(vocab['Part2'])",
     "random.choice(vocab['Adj2']) + ' ' + random.choice(vocab['Part0']) + ' ' + random.choice(vocab['Part2'])",
     "random.choice(vocab['Adj1']) + ' ' + random.choice(vocab['Adj2']) + ' ' + random.choice(vocab['Part0']) + ' ' + random.choice(vocab['Part1']) + ' ' + random.choice(vocab['Part2'])",
     "random.choice(vocab['Adj1']) + ' ' + random.choice(vocab['Adj2']) + ' ' + random.choice(vocab['Part0']) + ' ' + random.choice(vocab['Part1'])",
     "random.choice(vocab['Adj1']) + ' ' + random.choice(vocab['Adj2']) + ' ' + random.choice(vocab['Part1']) + ' ' + random.choice(vocab['Part2'])",
     "random.choice(vocab['Adj1']) + ' ' + random.choice(vocab['Adj2']) + ' ' + random.choice(vocab['Part0']) + ' ' + random.choice(vocab['Part2'])"]
    return '<Subject> ' + eval(random.choice(gadget)) + ' has ' + random.choice(vocab['VerbPT']) + ', ' + random.choice(vocab['Causing']) + ' ' + random.choice(vocab['VerbNow']) + ' in the ' + eval(random.choice(gadget)) + '!'


def generate_positive_outcome():
    return generate_outcome().replace('<Subject>', 'Their')


def generate_negative_outcome():
    return generate_outcome().replace('<Subject>', 'The')


def attack_rand(diff):
    logging.info('Generating random death result')
    difftxt = [(generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True),
     (generate_positive_outcome(), True)]
    for i in xrange(diff):
        difftxt.append((generate_negative_outcome() + '\n\nYour blood is boiling.', False))

    return random.choice(difftxt)


def simple_demo(*args, **kwargs):
    try:
        return _simple_demo(*args, **kwargs)
    except AttributeError:
        logging.warning('Bypassing a known error during battles')
        diff_bin = []
        if 'diff' not in kwargs:
            cur = random.choice(((generate_positive_outcome(), True), ("Their weapon hits a weak point in your ship's structure, and you take one last breath of air before you are sucked out into space.\n\nYour blood is boiling.", False)))
        else:
            cur = attack_rand(kwargs['diff'])
        print cur[0]
        return cur[1]


main = simple_demo
if __name__ == '__main__':
    simple_demo()
