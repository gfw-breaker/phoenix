#!/bin/bash

## main
source /etc/profile
cd /root/phoenix

node=$(/usr/sbin/ifconfig eth0 | grep 'inet ' | awk '{print $2}')

/usr/bin/python3 py/report-load.py $node


