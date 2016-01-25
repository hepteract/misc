class Game(object):
    '''The main code for running the game.'''

    def game(self):
        pass

    def __init__(self):
        self.health = 100
        self.attack = 10
        self.damage = 10
        self.game()
        
    def play(self):
        print self.introduction

        while True:
            print
            print self.location.description

            for event in self.location.events:
                self.health += event.process()
                myEvent = event.run()
                if myEvent:
                    try:
                        myEvent.isPlace()
                        self.location = event.run()
                    except:
                        myEvent.fight()
                if self.health <= 0:
                    print "That's it for you!"
                    exit(1)
                elif self.health > 200:
                    print "You are full of energy."
                    self.health = 200

            print 'Health: %d' % self.health
            self._transition()

    def _transition(self):
        transitions = self.location.transitions
        print 'You can go to these places:'
        for (index, transition) in enumerate(transitions):
            print index + 1, transition.title

        while True:
            try:
                choice = int(input('Choose one, or 0 to exit: '))
                if choice == 0:
                    break
                else:
                
                    self.location = transitions[choice - 1]
                    break
    
            except:
                print
                print "That's not a valid choice."
                print

        if choice == 0:
            exit()
