#!/usr/bin/python2.7

class NetworkInterface(object):
    def __init__(self, addr = None, peers = None):
        self.addr = addr if addr is not None else self.generate_address()
        self.peers = peers if peers is not None else []
        
        self.add_peer = self.peers.append

    def generate_address(self):
        addr = hex(id(self))
        return int(addr[10:], 16)

    def send(self, *msg):
        for peer in self.peers:
            print peer.f
            peer.send("".join(msg))
            peer.flush()

    def recv(self):
        msg = []
        for peer in self.peers:
            msg.append(peer.read())
        return "\n".join(msg)

class peer(object):
    def __init__(self, name, mode = "r"):
        self.f = file(name, mode) if type(name) is str else name
        self.send = self.f.write
        self.recv = self.f.read

    def __getattr__(self, name):
        return getattr(self.f, name)
open = peer
