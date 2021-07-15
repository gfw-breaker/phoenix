#!/bin/bash

source /etc/profile
cd /root/phoenix

python3 py/get-domains.py | grep "mapping:" > domains.txt

while read line; do
	path=$(echo $line | cut -d':' -f2)
	domain=$(echo $line | cut -d':' -f3)
	sed -e "s/templatePath/$path/g" -e "s/domainName/$domain/g" /etc/nginx/host.txt > /etc/nginx/conf.d/$path.host
done < domains.txt

service nginx reload

