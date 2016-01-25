from engine.event import Event
from engine.place import Place
from engine.battle import Battle
from engine.game import Game
from engine.action import Action
class test(Game):
    def game(self):
        self.introduction = '''
Welcome to test.
'''

        home = Place('House', "Welcome to your home.", ())
        outside = Place('Backyard', "Welcome to your backyard.", ())
        home.transitions = (outside,)
        outside.transitions = (home,)

        self.location = home
adv = test()
adv.play()