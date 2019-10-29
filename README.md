# ARP spoofing attack

This repository contains two files for creating an attack based on spoofing mac addresses:
- first one uses the arpspoof tool from Kali
[Usage]: ./arspoof\_kali.sh attack ip\_victim ip\_other\_host (DF gateway or any host from the same LAN)
This starts the arp spoofing attack, puts in backgroud the processes and prints to output the PIDs.

In order to stop it: ./arpspoof\_kali.sh clean pid\_proc pid\_proc2
This firstly cleans the arp tables on both sides, then stops the tools.

- the second one is an arpspoof attack created in python using the scapy library
[Usage]: python arp\_spoof\_attack.py attack/clean
The hw and ip addresses are added directly in code. When using attack flag, the arp tables
from both hosts are spoofed with the mac address of the Kali Linux.
With clean flag, the attack is stoped and the tables are cleaned as it in the last case.
The packets are sent from victim <---> Kali and from Kali <---> other host at a rate
of 3 seconds (2 arp replies - sleep 3sec - 2 arp replies etc.)
