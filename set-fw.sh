#!/bin/bash

yum remove -y firewalld
yum install -y iptables-services ipset-service initscripts

systemctl enable ipset
systemctl enable iptables

systemctl start ipset
systemctl start iptables

# cf
ipset -N cf hash:net
wget https://www.cloudflare.com/ips-v4 -O cf.txt
while read line; do
	ipset -A cf $line
done < cf.txt

# mgmt
ipset -N mgmt hash:net
while read ip; do
	ipset -A mgmt $ip
done < mgmt.txt

service ipset save

# check rules
iptables -L | grep 'cf src'
if [ $? -ne 0 ]; then
	iptables -I INPUT -m set --match-set cf src -j ACCEPT
fi

iptables -L | grep 'mgmt src'
if [ $? -ne 0 ]; then 
	iptables -I INPUT -p tcp --dport 22 -j DROP
	iptables -I INPUT -m set --match-set mgmt src -j ACCEPT
fi


service iptables save
service iptables reload


