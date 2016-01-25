name = raw_input("What do you want your project to be called? ")
script = name + ".py"
project = open(script, "w")
code = """
from engine.event import Event
from engine.place import Place
from engine.battle import Battle
from engine.game import Game
from engine.action import Action

class """, name, """(Game):
    def game(self):
        self.introduction = '''
Welcome to """, name, """.
'''

        home = Place('House', "Welcome to your home.", ())

        home.transitions = (,)

        self.location = home

adv = """, name, """()
adv.play()"""
project.write("from engine.event import Event")
project.write("\n")
project.write("from engine.place import Place")
project.write("\n")
project.write("from engine.battle import Battle")
project.write("\n")
project.write("from engine.game import Game")
project.write("\n")
project.write("from engine.action import Action")
project.write("\n")
project.write("class " + name + "(Game):")
project.write("\n")
project.write("    def game(self):")
project.write("\n")
project.write("        self.introduction = '''")
project.write("\n")
project.write("Welcome to " + name + ".")
project.write("\n")
project.write("'''")
project.write("\n")
project.write("")
project.write("\n")
project.write("""        home = Place('House', "Welcome to your home.", ())""")
project.write("\n")
project.write("""        outside = Place('Backyard', "Welcome to your backyard.", ())""")
project.write("")
project.write("\n")
project.write("        home.transitions = (outside,)")
project.write("\n")
project.write("        outside.transitions = (home,)")
project.write("\n")
project.write("")
project.write("\n")
project.write("        self.location = home")
project.write("\n")
project.write("adv = " + name + "()")
project.write("\n")
project.write("adv.play()")
