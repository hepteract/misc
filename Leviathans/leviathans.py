#Embedded file name: leviathans.pyc
from progressbar import ProgressBar
import logging
import random
import time
import sys
import os
logging.basicConfig(filename='leviathans.log', format='%(asctime)s @ %(filename)s> %(levelname)s: %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')
if __name__ != '__main__':
    logging.debug('%s imported', __name__)
custom_first_names = ('Ro',
 'Reginald',
 'Molly',
 'Jasmine',
 'Jasmin',
 'Virgil',
 'Abigal',
 'Ben',
 'Colin',
 'Tarquin',
 'Charles',
 'Charlie',
 'Patrick',
 'Darth',
 'Gates',
 'Bill',
 'Benjamin',
 'Brian',
 'Bryan',
 'William',
 'Janet',
 'Will',
 'Wil',
 'Aidan',
 'Weasley',
 'Allan',
 'Greg',
 'James',
 'Rosa',
 'Beverly',
 'Jean-luc',
 'Teddy',
 'Elias',
 'Elijah',
 'Aaron',
 'Erin',
 'Fred',
 'Toby',
 'Kate',
 'Ellie',
 'Caroline',
 'Madeline',
 'Katherine',
 'Suzy',
 'Sally',
 'Robert',
 'Lindsey',
 'Julia',
 'Sheila',
 'Allie',
 'Kelson',
 'Rachel',
 'Elle',
 'Morgan',
 'Chloe',
 'Zoe',
 'Johanna',
 'Nat',
 'Nathan',
 'Natalie',
 'Mo',
 'Monroe',
 'Jesse',
 'Jessie',
 'Keegan',
 'Ela',
 'Ella',
 'Alex',
 'Alexander',
 'Alexandra',
 'Lexi',
 'Dylan',
 'Dillan',
 'Josh',
 'Joshua',
 'John',
 'Joe',
 'Bob',
 'Rob',
 'Sasha',
 'Sascha',
 'Aria',
 'Daria',
 'Laria',
 'Lindsay',
 'Skyler',
 'Theo',
 'Skylar',
 'Charlotte',
 'Sing',
 'Santosh',
 'Phin',
 'Finn',
 'Miles',
 'Barbara',
 'Denise')
add_names = tuple(open('add_names.csv').read().split('\n'))
add_first_names = tuple(open('add_first_names.csv').read().split('\r'))
first_names = custom_first_names + add_names + add_first_names
first_names = tuple([x.strip("\n\r") + " " for x in first_names])
custom_last_names = ('VanNewkirk',
 'Laren',
 'Hamburg',
 'Newkirk',
 'Barclay',
 'Smith',
 'Jones',
 'Kirk',
 'Picard',
 'Janeway',
 'Gates',
 'Stewart',
 'Cisco',
 'Whitmer',
 'Harris',
 'McFadden',
 'Vader',
 'Bader',
 'McDonald',
 'MacDonald',
 'Kierstead',
 'Flynt',
 'Piper',
 'Riker',
 'Johnson',
 'Wheaton',
 'Crusher',
 'Fox',
 'Carpenter',
 'Capestany',
 'Okner',
 'Lin',
 'Rourke',
 'Xephos',
 'Schorsh',
 'Park',
 'Doe',
 'Kid',
 'Lord',
 'Miller',
 'Linker',
 'Smith',
 'Miller',
 'Blow',
 'Quiet',
 'Bean')
add_last_names = tuple(open('add_last_names.csv').read().split('\r'))
last_names = custom_last_names + add_last_names
last_names = tuple([x.strip("\n\r") for x in last_names])
random_ranks = ('Crewman',
 'Crewman',
 'Crewman',
 'Crewman',
 'Crewman',
 'Crewman',
 'Petty Officer',
 'Petty Officer',
 'Petty Officer',
 'Chief Petty Officer',
 'Ensign',
 'Ensign',
 'Ensign',
 'Lieutenant Junior Grade',
 'Lieutenant',
 'Lieutenant',
 'Lieutenant',
 'Petty Officer',
 'Petty Officer',
 'Petty Officer',
 'Chief Petty Officer',
 'Ensign',
 'Ensign',
 'Ensign',
 'Lieutenant Junior Grade',
 'Lieutenant',
 'Lieutenant',
 'Lieutenant',
 'Petty Officer',
 'Petty Officer',
 'Petty Officer',
 'Chief Petty Officer',
 'Ensign',
 'Ensign',
 'Ensign',
 'Lieutenant Junior Grade',
 'Lieutenant',
 'Lieutenant',
 'Lieutenant',
 'Petty Officer',
 'Petty Officer',
 'Petty Officer',
 'Chief Petty Officer',
 'Ensign',
 'Ensign',
 'Ensign',
 'Lieutenant Junior Grade',
 'Lieutenant',
 'Lieutenant',
 'Lieutenant',
 'Lieutenant Commander',
 'Petty Officer',
 'Petty Officer',
 'Petty Officer',
 'Chief Petty Officer',
 'Ensign',
 'Ensign',
 'Ensign',
 'Lieutenant Junior Grade',
 'Lieutenant',
 'Lieutenant',
 'Lieutenant',
 'Lieutenant Commander',
 'Petty Officer',
 'Petty Officer',
 'Petty Officer',
 'Chief Petty Officer',
 'Ensign',
 'Ensign',
 'Ensign',
 'Lieutenant Junior Grade',
 'Lieutenant',
 'Lieutenant',
 'Lieutenant',
 'Lieutenant Commander',
 'Commander')
flag_ranks = random_ranks + ('Captain',
 'Captain',
 'Captain',
 'Captain',
 'Captain',
 'Captain',
 'Captain',
 'Commodore',
 'Rear Admiral Lower Half',
 'Rear Admiral Lower Half',
 'Rear Admiral',
 'Rear Admiral',
 'Rear Admiral',
 'Vice Admiral',
 'Admiral',
 'Fleet Admiral')
ranks = ('Crewman',
 'Petty Officer',
 'Chief Petty Officer',
 'Ensign',
 'Lieutenant Junior Grade',
 'Lieutenant',
 'Lieutenant Commander',
 'Commander',
 'Captain',
 'Commodore',
 'Rear Admiral Lower Half',
 'Rear Admiral',
 'Vice Admiral',
 'Admiral',
 'Fleet Admiral')
roman_nums = (['M', 1000],
 ['CM', 900],
 ['D', 500],
 ['CD', 400],
 ['C', 100],
 ['XC', 90],
 ['L', 50],
 ['XL', 40],
 ['X', 10],
 ['IX', 9],
 ['V', 5],
 ['IV', 4],
 ['I', 1])

def int_to_roman(integer):
    returnlist = []
    for rom, num in roman_nums:
        while integer - num >= 0:
            integer -= num
            returnlist.append(rom)

    return ''.join(returnlist)


class CrewWeapon(object):

    def __init__(self, strength):
        self.__str = strength

    @property
    def str(self):
        return self.__str


class CrewMember(object):

    def __init__(self, name, rank = 'Petty Officer', vital = 5, nonvital = 20, skin = 100, equip = []):
        self.vital_organs = vital
        self.nonvital_organs = nonvital
        self.skin = skin
        self.name = name
        self.rank = rank
        self.equip = equip
        self.alive = True

    def __getWeapons(self):
        weap = []
        for item in self.equip:
            if type(item) == CrewWeapon:
                weap.append(item)

        return weap

    weap = property(__getWeapons)

    def __str__(self):
        return (self.rank + ' ' if self.rank not in ('', ' ') else '') + self.name + (' (DEAD)' if not self.alive else '')

    def __repr__(self):
        if self.alive:
            return '<Living ' + (self.rank + ' ' if self.rank not in ('', ' ') else 'Civilian ') + 'object: ' + self.name + '>'
        else:
            return '<Dead ' + (self.rank + ' ' if self.rank not in ('', ' ') else 'Civilian ') + 'object: ' + self.name + '>'

    def attack(self, enemy):
        if self.weap:
            enemy.dmg(random.choice(self.weap).str)
        elif self.alive:
            enemy.dmg(max(self.nonvital_organs / 100 * self.skin, 1))

    def dmg(self, amount):
        if amount > self.skin * 10:
            self.skin = 0
            self.vital_organs = 0
            self.nonvital_organs = 0
        else:
            if self.skin > 0:
                self.skin -= amount
            if amount > self.skin / 50:
                if self.nonvital_organs and self.vital_organs:
                    if random.randrange(0, 30) > self.nonvital_organs:
                        self.vital_organs -= 1
                    else:
                        self.nonvital_organs -= 1
                elif self.vital_organs:
                    self.vital_organs -= 1
                elif self.nonvital_organs:
                    self.nonvital_organs -= 1
            elif self.skin:
                self.skin -= amount / 10
        logging.debug('%s %s recieved %i damage', self.rank, self.name, amount)
        self.update()

    def update(self):
        if self.vital_organs < 4 or self.nonvital_organs < 4:
            logging.info(self.name + 'dead')
            self.alive = False

    def __eq__(self, other):
        if type(other) == CrewMember:
            return self.name == other.name
        elif type(other) == str:
            return self.name == other
        else:
            return None


class CrewRoster(list):

    def __repr__(self):
        return '<CrewRoster object consisting of ' + str(len(self)) + ' personnel>'

    def __str__(self):
        string = ''
        for o in self:
            string += str(o)
            string += '\n'

        return string

    def get_random_crewmember(self):
        crew = CrewMember('Guy', rank='Red Shirt')
        crew.alive = False
        while not crew.alive:
            random_crew_id = random.randrange(0, len(self))
            crew = self[random_crew_id - 1:random_crew_id][0]

        return crew

    def fight(self, enemy, out = None):
        side0 = CrewRoster(self)
        side1 = CrewRoster(enemy)
        side0_leader = side0[0]
        side1_leader = side1[0]
        logging.info("Fight in progress between %s's team and %s's team.", str(side0_leader), str(side1_leader))
        while side0 and side1:
            for o in side0:
                for e in side1:
                    if o.alive:
                        o.attack(e)
                    if e.alive and o.alive:
                        logging.debug(o.name + ' attacks ' + e.name + '\n')
                    elif o.alive:
                        logging.debug(o.name + ' attacks and kills ' + e.name + '\n')
                        side1.pop(side1.index(e))
                    if e.alive:
                        e.attack(o)
                    if o.alive and e.alive:
                        logging.debug(e.name + ' attacks ' + o.name + '\n')
                    elif e.alive:
                        logging.debug(e.name + ' attacks and kills ' + o.name + '\n')
                        side0.pop(side0.index(o))
                    if not o.alive:
                        break
                        time.sleep(0.1)

        if side0:
            print str(side0_leader) + "'s team defeated", str(side1_leader) + "'s team"
            logging.info("%s's team defeated %s's team", str(sideo0_leader), str(side1_leader))
        elif side1:
            print str(side1_leader) + "'s team defeated", str(side0_leader) + "'s team"
            logging.info("%s's team defeated %s's team", str(sideo0_leader), str(side1_leader))


def generate_crew_roster(num = 5000, captain = None, weapon = None, ranks = True):
    if ranks != "flag":
        global random_ranks
    else:
        random_ranks = flag_ranks
    
    roster = CrewRoster()
    roster_dict = {}
    pbar = ProgressBar()
    if not captain:
        roster.append(CrewMember(random.choice(first_names) + random.choice(last_names), 'Captain' if ranks else ''))
    else:
        roster.append(CrewMember(captain, 'Captain' if ranks else ''))
    for i in xrange(num - 1):
        name = random.choice(first_names) + random.choice(last_names)
        if name in roster_dict:
            roster_dict[name] += 1
            roster.append(CrewMember(name + " " + int_to_roman(roster_dict[name]), random.choice(random_ranks) if ranks else ''))
        else:
            roster_dict[name] = 1
            roster.append(CrewMember(name, random.choice(random_ranks) if ranks else ''))

    return roster


def generate_crew_roster_file(num = 5000, captain = None, name = 'roster.txt', ranks = True):
    rosterfile = open(name, 'w')
    crew = generate_crew_roster(num, captain, None, ranks)
    for o in crew:
        rosterfile.write(str(o))
        rosterfile.write('\n')


def generate_planet_file(mult = 1, ranks = False, name = 'planet.txt'):
    return generate_crew_roster_file(mult * 100000, ranks=ranks, name=name)

class ShipModule(object):

    def __init__(self, hp = 100, func = 'hull', symbol = None, crew = CrewRoster(), **data):
        self.hp = hp
        self.func = func
        self.data = data
        self.layer = None
        self.symbol = symbol
        self.crew = CrewRoster(crew)

    def link(self, layer):
        self.layer = layer

    def dmg(self, mag):
        logging.debug('Ship module damaged')
        if self.hp > mag:
            self.hp -= mag
        else:
            self.hp = 0
            self.func = False
            for human in self.crew:
                human.skin = human.vital_organs = human.nonvital_organs = 0
                human.alive = False

    def activate(self, target):
        logging.debug('Ship module activated')
        if self.func == 'dmg':
            target.dmg(self.data['mag'], self.data['axis'], self.data['pos'] + self.layer.offset(target, self.data['axis']))
            return True
        if self.func == 'scn':
            if random.randrange(0, 10) == 5:
                return self.layer
            else:
                return target
        elif self.func == 'mov':
            if self.data['type'] == 'rotate':
                self.layer.rotate_course()
            elif self.data['type'] == 'thrust':
                self.layer.accelerate(self.data['mag'] * self.data['dir'])

    def __repr__(self):
        if self.func == 'dmg':
            return '<' + ('Functioning' if self.hp else 'Non-functioning') + ' Weapons Array>'
        elif self.func == 'scn':
            return '<' + ('Functioning' if self.hp else 'Non-functioning') + ' Sensor Array>'
        elif self.func == 'mov':
            return '<' + ('Functioning' if self.hp else 'Non-functioning') + ' Engines>'
        elif self.func == 'hull':
            return '<' + ('Functioning' if self.hp else 'Non-functioning') + ' Hull Plating>'
        elif self.func:
            return '<' + ('Functioning' if self.hp else 'Non-functioning') + ' ' + self.func + '>'
        else:
            return 'None'

    def __str__(self):
        if self.hp > 0:
            if self.symbol:
                return self.symbol
            elif self.func == 'dmg':
                return '$'
            elif self.func == 'scn':
                return '%'
            elif self.func == 'mov':
                return '^'
            elif self.func == 'hull':
                return '='
            else:
                return ' '
        else:
            if self.func is None:
                return ' '
            return '*'


class ShipLayer(object):

    def __init__(self, layermap, ship_x = 0, ship_y = 0):
        self.map = layermap
        self.x = ship_x
        self.y = ship_y
        self.velocity = [0, -1]
        for y in layermap:
            for module in y:
                module.link(self)

    def board(self, party, out = None):
        logging.info('Boarding parties sent')
        board = random.choice(random.choice(self.map))
        board.crew.fight(party, out)
        crew_alive = True
        for o in board.crew:
            if o.alive:
                crew_alive = True
                break

        if not crew_alive:
            board.func = False
            board.symbol = '%'

    def dmg(self, dmg_mag, dmg_axis, dmg_pos):
        logging.debug('Ship damaged')
        target = None
        if dmg_axis == 0:
            x_increment = 0
            y_increment = 0
            while not target or not target.hp:
                try:
                    target = self.map[y_increment][dmg_pos + x_increment]
                    y_increment += 1
                except IndexError:
                    return ShipModule(func=None)

        if dmg_axis == 1:
            x_increment = 0
            y_increment = 0
            while not target or not target.hp:
                try:
                    target = self.map[dmg_pos + y_increment][x_increment]
                    x_increment += 1
                except IndexError:
                    return ShipModule(func=None)

        if target:
            target.dmg(dmg_mag)

    def accelerate(self, mag):
        logging.info('Ship accelerating (without using engines)')
        self.velocity[0] += mag
        self.update()

    def rotate_course(self):
        logging.info('Ship rotating (without using engines)')
        self.velocity[1] = -self.velocity[1]
        self.update()

    def update(self):
        if self.velocity[1] == -1:
            self.x += self.velocity[0]
        elif self.velocity[1] == 1:
            self.y += self.velocity[0]

    def offset(self, other, axis = None):
        if axis == 1:
            return self.y - other.y
        elif axis == 0 or axis == -1:
            return self.x - other.x
        else:
            return (self.x - other.x, self.y - other.y)

    def attack(self, target):
        logging.info('Ship attacking')
        for y in self.map:
            for module in y:
                if module.func == 'dmg':
                    module.activate(target)

        self.update()

    def __repr__(self):
        return str(self.map)

    def __str__(self):
        map_str = ''
        for y in self.map:
            y_str = ''
            for module in y:
                y_str += str(module)

            map_str += y_str + '\n'

        return map_str
