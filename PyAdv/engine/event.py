from random import random

class Event(object):
    '''A game event, including the probability of its happening.'''

    def __init__(self, probability, message, healthChange, maxOccur=100000, go = None, battle = None):
        self.probability = probability
        self.message = message
        self.healthChange = healthChange
        self.remainingOccur = maxOccur
        self.go = go
        self.battle = battle

    def process(self):
        '''Process the event, and return the change in health, or 0.'''

        self.rand = random()
        if self.remainingOccur and self.rand < self.probability:
            self.remainingOccur -= 1
            print self.message
            return self.healthChange

        return 0

    def run(self):
        '''Send the player somewhere'''

        can_do = self.remainingOccur + 1
        if can_do and self.rand < self.probability:
            if self.go:
                return self.go
            else:
                return self.battle


