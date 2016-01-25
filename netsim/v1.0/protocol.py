from abc import ABCMeta, abstractmethod, abstractproperty
from operator import itemgetter

import collections
import struct
import random
import time
import rsa

class Protocol(object):
    __metaclass__ = ABCMeta
    def __init__(self, interface):
        self.int = interface
        self._read = []

    @abstractmethod
    def read(self, num):
        pass

    @abstractmethod
    def write(self, contents):
        pass

class HermesProtocol(Protocol):
    fmt = 'HfII%len%s' # packet id -- timestamp -- dest addr -- source addr -- contents
    _handshake = "HELLO"
    stringlen = 128

    tuple = collections.namedtuple("HermesPacket", ('id', 'timestamp', 'dest', 'source', 'content', 'magic') )
    
    def __init__(self, interface, address = None, promiscuous = False):
        if address:
            self.addr = address
        else:
            self.addr = interface.addr
        self.id = 0
        self.prom = promiscuous
        super(HermesProtocol, self).__init__(interface)

    def read(self, num = -1):
        packets = []
        for packet in self.int.recv().split("\n"):
            if packet[2:4] == 'hp' and packet not in self._read:
                len_str = struct.unpack('I', packet[4:8])
                fmt = self.fmt.replace('%len%', str(len_str[0]))
                #print fmt
                
                data = list(struct.unpack(fmt, packet[8:]))

                data[4] = data[4].strip('\0')

                data.append(packet[:2])
                
                if data[2] == self.addr or self.prom:
                    if data[4] == self._handshake:
                        data[0] = -1
                    packets.append(self.tuple(*data))
        packets = sorted(packets, key = itemgetter(0))

        if num == -1:
            self._read = self._read + packets
            return packets
        else:
            self._read = self._read + packets[:num]
            return packets[:num]

    def write(self, dest, contents, protocol = '\0\0', pid = None, timestamp = None):
        if pid is None:
            pid = self.id
            self.id += 1
        if timestamp is None:
            timestamp = time.time()
        fmt = self.fmt.replace('%len%', str(len(contents)))
        packet = protocol + 'hp' + struct.pack('I', len(contents)) + struct.pack(fmt, pid, timestamp, dest, self.addr, contents)
        self.int.send(packet, "\n")
        #return packet

    def handshake(self, dest, magic = '\0\0'):
        self.id = 0
        self.write(self, dest, self._handshake, magic)
"""
class InterCellRoutingProtocol(Protocol):
    fmt = 'II%len%s2s' # dest - source - content - magic
    regfmt = 'I' # icrp address
    tuple = collections.namedtuple("RouterPacket", ('id', 'timestamp', 'dest', 'source', 'content', 'magic')) # id and timestamp are stored in parent (Hermes) packet
    
    def __init__(self, interface, address, router, protocol = None):
        if not protocol:
            protocol = HermesProtocol
        self.int = protocol(interface)
        self.addr = address
        self.router = router
        
        self.packets = []

        self.int.write(self.router, struct.pack(self.regfmt, address), 'rn')

    def write(self, dest, content, protocol = '00', pid = None, timestamp = None):
        fmt = self.fmt.replace('%len%', str(len(content)))
        packet = struct.pack('I', len(content)) + struct.pack(fmt, dest, self.addr, content, protocol)
        self.int.write(self.router, packet, 'ic', pid, timestamp)

    def read(self, num = -1):
        for packet in self.int.read():
            if packet.magic == 'ic': # inter-cell
                strlen = struct.unpack('I', packet.content[:4])
                fmt = self.fmt.replace('%len%', str(strlen))
                data = self.tuple( struct.unpack(fmt, packet.content[4:]) )

                self.packets.append(data)
        if num == -1:
            packets = self.packets
            self.packets = []
        else:
            packets = self.packets[:num]
            self.packets = self.packets[num:]
        return packets
                

class InterCellRoutingProtocol_Router(InterCellRoutingProtocol):
    timeout = 60
    
    def __init__(self, interface_protocol, keys = None, links = {}, clients = {}):
        self.clients = clients.copy()
        self.links = links.copy()
        if keys:
            self.pub = keys[0]
            self.prv = keys[1]
        else:
            self.pub, self.prv = rsa.newkeys(128)
        self.int = interface_protocol
        self._read = []

    def update(self):
        for packet in self.int.read():
            if packet.magic == "ic": # inter-cell
                strlen = struct.unpack('I', packet.content[:4])
                fmt = self.fmt.replace('%len%', str(strlen))
                data = self.tuple( struct.unpack(fmt, packet.content[4:]) )

                if data.dest in self.clients and packet not in self._read:
                    self.int.write(self.clients[data.dest], packet.content, 'ic', packet.id, packet.timestamp)
                    self.read.append(packet)

                elif data.timestamp + self.timeout > time.stamp:
                    for router, interface in self.link.items():
                        interface.write(router, packet.content, 'ic', packet.id, packet.timestamp)
            elif packet.magic == 'rn': # register node
                addr = struct.unpack(self.regfmt, packet.content)[0]
                self.clients[addr] = packet.source
        """
