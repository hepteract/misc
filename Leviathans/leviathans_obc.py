#Embedded file name: leviathans_obc.pyc
import leviathans_world as game
import leviathans_planets as lp
import sys

def multiline_input(prompt = ''):
    input = ''
    input += raw_input(prompt)
    last = raw_input(prompt)
    while last != '':
        input += '\n'
        input += last
        last = raw_input(prompt)

    return input


class FakeInput(object):

    def __init__(self, sys, stdin, script):
        self.sys = sys
        self.stdin = stdin
        self.script = script

    def readline(self):
        if len(self.script) > 0:
            return self.script.pop(0)
        else:
            self.sys.stdin = self.stdin
            return self.stdin.readline()


class OnboardComputer(object):

    def __init__(self):
        self.scripts = {}

    def run(self, script):
        sys.stdin = FakeInput(sys, sys.stdin, script.split('\n'))


computer = OnboardComputer()

def script(world, cmd, playerid):
    computer.scripts[cmd.strip('script')[1:]] = multiline_input('> ')


game.new_cmd['script'] = script

def run(world, cmd, playerid):
    try:
        computer.run(computer.scripts[cmd.strip('run')[1:]])
    except KeyError:
        print "Sorry, that script doesn't exist."


game.new_cmd['run'] = run
main = lp.main
if __name__ == '__main__':
    main()
