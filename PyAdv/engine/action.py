from random import random

class Action(object):
    '''A game event, including the probability of its happening.'''

    def __init__(self, description, message, healthChange, maxOccur=100000, go = None, battle = None, script = None):
        self.message = message
        self.description = description
        self.healthChange = healthChange
        self.remainingOccur = maxOccur
        self.go = go
        self.battle = battle

    def process(self):
        '''Process the action, and return the change in health, or 0.'''

        if self.remainingOccur:
            self.remainingOccur -= 1
            prompt = "Do you want to ", self.description, "(y or n)?"
            do = raw_input(prompt)
            if do == "y":
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

    def display(self):
        '''Display the name of the action'''

        print self.description
        return True


