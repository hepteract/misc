class Place(object):
    def __init__(self, title, description, events, transitions = ()):
        self.title = title
        self.description = description
        self.events = events
        self.transitions = transitions

    def isPlace(self):
        pass
