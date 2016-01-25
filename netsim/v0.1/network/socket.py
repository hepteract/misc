import protocol
import time
import collections

protocols = {"hermes" : protocol.HermesProtocol}


class socket(object):
    def __init__(self, interface, protocol = "hermes", magic = "\0\0"):
        if type(protocol) is str:
            self.protocol = protocols[protocol](interface)
        else:
            self.protocol = protocol(interface)
        self.magic = magic
        self._open = False
        
    def open(self, addr, wait = 10):
        self.dest = addr
        
        self.protocol.handshake(self.dest, self.magic)
        
        end_time = time.time() + wait
        
        while time.time() > cur_time:
            packet = self.protocol.read(1)

            if packet.id == -1 and packet.dest == self.dest:
                return self
        return None

    def write(self, msg):
        if len(msg) <= self.protocol.stringlen:
            self.protocol.write(self.dest, msg, self.magic)
        else:
            while len(msg) > self.protocol.stringlen:
                self.protocol.write(self.dest, msg[:self.protocol.stringlen], self.magic)
                msg = msg[self.protocol.stringlen:]

    def read(self, bytes = 0):
        packets = self.protocol.read(bytes / self.protocol.stringlen)
        string = ""

        for packet in packets:
            string += packet.content
        return string[:bytes]
