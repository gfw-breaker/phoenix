#!/bin/bash

url="https://www.cloudflare.com/ips-v4"

wget $url -O cidrs.txt

firewall-cmd --permanent --new-ipset=cf --type=hash:net
firewall-cmd --permanent --ipset=cf --add-entries-from-file=cidrs.txt



#firewall-cmd --permanent --new-ipset=mgmt --type=hash:net


