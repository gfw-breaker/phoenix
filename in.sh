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
cp -f "$tmp_dir/systemd/system/v2ray.service" "/lib/systemd/system/"


# generate config
config_dir=/usr/local/etc/v2ray
mkdir -p $config_dir
uuid=$(v2ctl uuid)
cp -f config.json $config_dir



# setup nginx
yum install -y nginx

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout  /etc/nginx/server.key -out  /etc/nginx/server.crt -subj "/C=US/ST=Zhejiang/L=Hangzhou/O=mofei/OU=mofei/CN=v2ray.kkk"

cp nnew.conf /etc/nginx/nginx.conf

# start services
systemctl enable nginx
systemctl enable v2ray
systemctl start nginx
systemctl start v2ray




