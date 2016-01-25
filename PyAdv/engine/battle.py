from random import randrange, random
from time import sleep as wait

class Battle(object):
    """A battle scene"""

    def __init__(self, game, enemy_health = 50, enemy_attack = 5, enemy_damage = 10):
        self.pc = game
        self.npc = [enemy_health, enemy_attack, enemy_damage]

    def fight(self):
        while self.npc[0] > 0 and self.pc.health > 0:
            npc_attack = randrange(0, self.npc[1])
            pc_attack = randrange(0, self.pc.attack)
            if npc_attack > pc_attack:
                print "Your opponent easily blocks your attack and hurts you."
                self.pc.health -= self.npc[2]
                wait(1)
            elif npc_attack == pc_attack:
                print "Your opponent just barely blocks your blow, and you theirs."
                print "Nothing happens."
                wait(1)
            elif npc_attack < pc_attack:
                print "You easily block your opponent's attack and you hit them."
                self.npc[0] -= self.pc.damage
                wait(1)

        if self.npc[0] < 0:
            print "You defeat your opponent."
