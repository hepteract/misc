import leviathans_world as game
import leviathans_planets as lp
import leviathans as core

import random
import copy

import logging
logging.basicConfig(filename='leviathans.log', format='%(asctime)s @ %(filename)s> %(levelname)s: %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

class Cell(object):
    def __init__ (self, map, desc = None, empty = None):
        self.map = map

        if empty is None:
            empty = random.choice((False, True))

        self.empty = empty

        if empty is True:
            self.desc = ""
            self.icon = " "
        elif desc is None:
            self.desc = "This is an empty room."
            self.icon = "#"
        else:
            self.desc = desc
            self.icon = "#"

    def __str__(self):
        return self.icon

class Map(object):
    def __init__(self, size = -1):
        if size == -1:
            size = random.randrange(5, 15)
            
        self.map = [ [Cell(self) for i in xrange(size)] for i in xrange(size)]

    def __str__(self):
        layout = copy.deepcopy(self.map)
        layout.reverse()

        for row in layout:
            row.reverse()
        
        string = []
        for row in layout:
            for cell in row:
                string.append(str(cell))
            string.append("\n")
        return "".join(string[:-1])

    def __getitem__(self, name):
        if type(name) is int:
            return self.map[name]
        else:
            return self.get_cell(name)

    def get_adjacent(self, cell, ignore_empty = True):
        if type(cell) is Cell:
            return tuple( [self.get_cell(item) for item in self.get_adjacent( self.find_cell(cell) )] )
        else:
            ret = []
            
            if cell[0] > 1:
                ret.append( (cell[0] - 1, cell[1]) )
            if cell[1] > 1:
                ret.append( (cell[0], cell[1] - 1) )
            if cell[0] > 1 and cell[1] > 1:
                ret.append( (cell[0] - 1, cell[1] - 1) )

            if cell[0] < (len(self.map) - 1):
                ret.append( (cell[0] + 1, cell[1]) )
            if cell[1] < (len(self.map) - 1):
                ret.append( (cell[0], cell[1] + 1) )
            if cell[0] < (len(self.map) - 1) and cell[1] < (len(self.map) - 1):
                ret.append( (cell[0] + 1, cell[1] + 1) )

            if ignore_empty:
                return tuple( [cell for cell in ret if not self.get_cell(cell).empty] )
            else:
                return tuple(ret)

    def get_cell(self, cell):
        return self.map[ cell[0] ][ cell[1] ]

    def find_cell(self, cell):
        for i, row in enumerate(self.map, 0):
            if cell in row:
                return (i, row.index(cell))
        return (False, False)

    def __contains__(self, value):
        for row in self.map:
            if value in row:
                return True
        if type(value) in (list, tuple):
            if value[0] >= 0 and value[1] >= 0 and value[0] < len(self.map) and value[1] < len(self.map):
                return True
        return False

class Station(object):
    def __init__(self, name):
        self.name = name
        
        self.crew = core.generate_crew_roster(random.randrange(10, 100),\
                                              ranks = False)
        self.crew += core.generate_crew_roster(random.randrange(5, 20),\
                                               ranks = "flag")

        self.map = Map()

    def __str__(self):
        return str(self.map)

class Player(object):
    def __init__(self, world):
        self.world = world
        self.coords = (0, 0)

    def play(self):
        cell = self.world.get_cell(self.coords)
        print cell.desc

        cmd = raw_input().lower()
