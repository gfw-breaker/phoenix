#!/bin/bash
# author: gfw-breaker(翻墙教练)

yum install -y unzip wget git net-tools epel-release socat netcat bind-utils

pkg_url="https://github.com/v2fly/v2ray-core/releases/download/v4.34.0/v2ray-linux-64.zip"
tmp_dir=/tmp/v2ray

mkdir -p $tmp_dir
wget $pkg_url -O v2ray.zip
unzip v2ray.zip -d $tmp_dir

cp $tmp_dir/v2ray /usr/local/bin
cp $tmp_dir/v2ctl /usr/local/bin


# enable daemon
cp -f "$tmp_dir/systemd/system/v2ray.service" "/lib/systemd/system/"
systemctl enable v2ray


# generate config
config_dir=/usr/local/etc/v2ray
mkdir -p $config_dir
uuid=$(v2ctl uuid)
cp -f config.json $config_dir


# get domain name, fail if DNS record is not created in 10 mins 
ip=$(/usr/sbin/ifconfig eth0 | grep "inet " | awk '{print $2}')
url=http://gfw-breaker.win/dns/$ip
for i in {1..20}; do
	domainname=$(curl $url)	
	echo $domainname | grep '//' > /dev/null
	if [ $? -eq 0 ]; then
		echo "DNS record is not created yet. Waiting ..."
		sleep 30
	else
		domainname=$(echo $domainname | head -n 1 | awk '{print $1}')	
		break
	fi
done


# check domain name can be resolved
for i in {1..20}; do
	host $domainname
	if [ $? -eq 0 ]; then
		break
	else
		echo "DNS record can't be resolved. Waiting ..."
		sleep 30
	fi
done


# setup nginx
yum install -y nginx

curl  https://get.acme.sh | sh 

/.acme.sh/acme.sh --issue -d $domainname --standalone
/.acme.sh/acme.sh --installcert -d $domainname  --fullchainpath /etc/ssl/v2ray.crt --keypath /etc/ssl/v2ray.key

sed -i "s/#domainname#/$domainname/g" nginx.conf > /etc/nginx/nginx.conf


# start services
service nginx restart
systemctl start v2ray




