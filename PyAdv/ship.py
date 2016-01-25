from engine.event import Event
from engine.place import Place
from engine.battle import Battle
from engine.game import Game
from engine.action import Action

class ShipGame(Game):
    def game(self):
        self.introduction = '''
Welcome to Ship Adventure. You are the captain of a star ship.
'''
        alien_fight = Battle(self)
        holobattle = Battle(self, 100, 6, 0)

        bridge = Place('Bridge',
            "You are on the bridge of a spaceship, sitting in the captain's chair.",
            (
            Event(0.01, 'An intruder beams onto the bridge and shoots you.\nIt starts to fight you.', -50, maxOccur = 1, battle = alien_fight),
            Event(0.1, "The ship's doctor gives you a health boost.", 30),
            ))

        readyRoom = Place('Ready Room', "You are in the captain's ready room.", ())

        quarters = Place('Captain\'s Quarters', 'Welcome to your quarters.', (
            Event(1, 'Relaxing in your quarters improves your health.', 20),
            Event(0.1, 'But you are paged to return to the bridge and you don\'t get to relax.\n You go to the bridge.', -20, go = bridge),
        ))

        broken_lift = Place('Lift', 'The turbolift is stuck', (
            Event(0.1, "The turbolift powers up.\nYou go to your quarters", 0, go = quarters),
        ))

        lift = Place('Lift', 'You have entered the turbolift.', (
            Event(0.05, "The ship's android says hello to you.", 0),
            Event(0.05, "The turbolift breaks down and goes falling through the shaft.\nYou break a rib", -25, go = broken_lift, maxOccur = 1),
        ))

        lounge = Place('Lounge', 'Welcome to the lounge.', (
            Event(1, 'Relaxing in the lounge improves your health.', 10),
        ))

        turboshaft = Place('Turbo Shaft', 'You climb down the ladder', (
            Event(0.6, 'Your rib throbs.', -2),
        ))

        vent = Place('A vent', 'You climb into the vent.\nYou can fit into the entrance but not the rest.', (
            Event(0.4, 'The floor of the vent collapses, and you fall into your quarters.\nYour rib throbs painfully.', -10, go = quarters),
        ))

        sickbay = Place('Sickbay',
            "You are in Sickbay.",
            (
            Event(0.8, "The ship's doctor gives you a health boost.", 30),
        ))

        engine = Place("Engineering","You are in Engineering.",(
            Event(0.05, "There is a warp core breach.\nYou are scalded by anti-matter.\nYou fall unconscious, and you are taken to Sickbay", -60, go = sickbay, maxOccur = 1),
        ))

        holodeck_on = Place("Holodeck", "You are in a holodeck program", (
            Event(0.99, "A man steps out of the shadows and shoots you.", 0, battle = holobattle),
        ))
        
        holodeck = Place('Holodeck',"Welcome to the Holodeck",(
            Event(0.8, "The Holodeck program begins", 0, go = holodeck_on),
        ))
            
        holodeck_arch = Place("Stop Program", "Welcome to the Holodeck", (
            Event(1, "The Holodeck program stops", 0, go = holodeck),
        ))

        cafe = Place("Starbucks", "You are in a cafe from the early 21st century", (
            Event(1, "Drinking a cup of coffee warms you up and improves your health", 10),
            Event(0.02, "A man steps out of the shadows and shoots you.", 0, battle = holobattle)
            
        ))
        bridge.transitions = (readyRoom, lift)
        readyRoom.transitions = (bridge,)
        lift.transitions = (bridge, lounge, quarters, sickbay, engine, holodeck)
        lounge.transitions = (lift,)
        quarters.transitions = (lift,)
        broken_lift.transitions = (turboshaft,)
        turboshaft.transitions = (broken_lift, vent)
        vent.transitions = (turboshaft,)
        sickbay.transitions = (lift,)
        engine.transitions = (lift,)
        holodeck.transitions = (lift,)
        holodeck_on.transitions = (holodeck_arch, cafe)
        cafe.transitions = (holodeck_arch, holodeck_on)

        self.location = bridge

adv = ShipGame()
adv.play()
