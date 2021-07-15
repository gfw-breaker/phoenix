#!/bin/bash

for i in {1..5000}; do
	path=$i.com
	domain=$i"_abc"
	echo $domain
	sed -e "s/templatePath/$path/g" -e "s/domainName/$domain/g" /etc/nginx/template.host > /etc/nginx/conf.d/$path.host
done


