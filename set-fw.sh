#!/bin/bash

url="https://www.cloudflare.com/ips-v4"

# Remove service
firewall-cmd --permanent --remove-service=ssh

wget $url -O cf.txt
# Allow CloudFlare
firewall-cmd --permanent --new-ipset=cf --type=hash:net
firewall-cmd --permanent --ipset=cf --add-entries-from-file=cf.txt

# Allow MGMT 
firewall-cmd --permanent --new-ipset=mgmt --type=hash:net
firewall-cmd --permanent --ipset=mgmt --add-entries-from-file=mgmt.txt


