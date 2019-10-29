# ARP spoofing attack

This repository contains two scripts for creating an attack based on spoofing MAC addresses:

**Shell script**:
```console
# first one uses the arpspoof tool from Kali
# [Usage] 
./arspoof_kali.sh attack ip_victim ip_other_host (DF gateway or any host from the same LAN)
```
This starts the arp spoofing attack, puts in backgroud the processes and prints to output the PIDs. 
```console
# In order to stop it: 
./arpspoof_kali.sh clean pid_proc pid_proc2
```
This firstly cleans the arp tables on both sides, then stops the tools.

**Scapy script**:
- the second one is an arpspoof attack created in python using the scapy library
```console
# [Usage]: 
python arp_spoof_attack.py attack/clean
```
The hw and ip addresses are added directly in code. When using attack flag, the arp tables
from both hosts are spoofed with the mac address of the Kali Linux.
With clean flag, the attack is stoped and the tables are cleaned as it in the last case.
The packets are sent from victim <---> Kali and from Kali <---> other host at a rate
of 3 seconds (2 arp replies - sleep 3sec - 2 arp replies etc.)

## Bibliography
Based on sources like: https://ourcodeworld.com/articles/read/422/how-to-perform-a-man-in-the-middle-mitm-attack-with-kali-linux
