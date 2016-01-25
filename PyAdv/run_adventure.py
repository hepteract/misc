#!/usr/bin/python2.7

from engine.event import Event
from engine.place import Place
from engine.battle import Battle
from engine.game import Game
from engine.action import Action

import json

class JSONParser(object):
    def __init__(self, code, game = None):
        self.data = json.loads(code)
        self.objects = {}
        self.events = {}
        self.battles = {}
        self.places = {}
        self.actions = {}

        if game is None:
            self.game = Game()
        else:
            self.game = game

    def parse(self):
        self.generate_objects()
        self.process_places()
        self.link_objects()
        self.spawn_player()

        return self.game

    def generate_objects(self):
        for name, obj in self.data.items():
            if type(obj) is dict:
                if obj["type"] == "event":
                    del obj["type"]
                    self.events[name] = self.objects[name] = Event(**obj)
                elif obj["type"] == "battle":
                    del obj["type"]
                    self.battles[name] = self.objects[name] = Battle(**obj)
                elif obj["type"] == "place":
                    del obj["type"]
                    self.places[name] = self.objects[name] = Place(**obj)
                elif obj["type"] == "action":
                    del obj["type"]
                    self.actions[name] = self.objects[name] = Action(**obj)

    def process_places(self):
        for place in self.places:
            trans = []
            for link in place.transitions:
                trans.append(self.places[link])
            place.transitions = tuple(trans)

            events = []
            for event in place.events:
                events.append(self.events[event])
            place.events = tuple(events)

    def link_objects(self):
        for obj in self.objects.values():
            for name, value in obj.__dict__.items():
                if type(value) is str:
                    if value.startswith("@"):
                        obj.__dict__[name] = self.objects[ value[1:] ]

    def spawn_player(self):
        self.game.location = self.places[ self.data["spawn"] ]

def main(filename):
    with open(filename + ".json") as jsonfile:
        code = jsonfile.read()

    lines = code.split("\n")
    code = []
    for line in lines:
        if not line.startswith("#"):
            code.append(line)
    
    parser = JSONParser("\n".join(code))
    game = parser.parse()
    game.play()

if __name__ == "__main__":
    main(raw_input("Adventure Name: "))
