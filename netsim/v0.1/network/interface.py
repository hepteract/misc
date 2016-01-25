import struct
import time
import os

expiry = {}

class NetworkInterface(object):
    def __init__(self, cell = '.', addr = None):
        self.cell = cell
        if addr:
            self.addr = addr
        else:
            self.addr = int( str(id(self))[10:] )
    
    def write(self, packet, contents = ""):
        with open( os.path.join( self.cell, packet ).encode("ascii", "ignore"), "w") as pfile:
            pfile.write( contents )
            expiry[packet] = time.time() + 60

    def read(self, packet = None):
        if packet:
            with open( os.path.join(self.cell, packet).encode("ascii", "ignore") ) as pfile:
                ret = pfile.read()
            return ret
        else:
            ls = os.listdir(self.cell)
            packets = []
            for packet in ls:
                if packet in expiry:
                    if expiry[packet] < time.time():
                        os.remove( os.path.join(self.cell, packet) )
                        continue
                packets.append(packet)
            return packets
                
