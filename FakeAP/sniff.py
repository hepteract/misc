#! /usr/bin/python

from scapy.all import *
import sys

def dns(pkt):
	if IP in pkt:
		ip_src = pkt[IP].src
		ip_dst = pkt[IP].dst	
		if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0 and ip_src != "10.20.86.254":
			print str(ip_src) + " -> " + str(ip_dst) + " : " + "(" + pkt.getlayer(DNS).qd.qname + ")"
def http(packet):
        if TCP in packet:
            ip = packet.getlayer(IP)
            tcp = packet.getlayer(TCP)

            print "%s:%d -> %s:%d" % (ip.src, tcp.sport, ip.dst, tcp.dport)
sniff(iface = "wlan0",filter = "port 53", prn = dns, store = 0)
print "\n[*] Shutting Down..."
