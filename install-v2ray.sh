#!/bin/bash

yum install -y unzip wget git net-tools epel-release socat netcat bind-utils

pkg_url="https://github.com/v2fly/v2ray-core/releases/download/v4.34.0/v2ray-linux-64.zip"
tmp_dir=/tmp/v2ray

mkdir -p $tmp_dir
wget $pkg_url -O v2ray.zip
unzip v2ray.zip -d $tmp_dir

cp $tmp_dir/v2ray /usr/local/bin
cp $tmp_dir/v2ctl /usr/local/bin
cp -f "$tmp_dir/systemd/system/v2ray.service" "/lib/systemd/system/"
sed -i '/nobody/d' /lib/systemd/system/v2ray.service


# generate config
config_dir=/usr/local/etc/v2ray
mkdir -p $config_dir
uuid=$(v2ctl uuid)
cp -f templates/config.json $config_dir


# setup nginx
yum install -y nginx

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout  /etc/nginx/server.key -out  /etc/nginx/server.crt -subj "/C=US/ST=Zhejiang/L=Hangzhou/O=mofei/OU=mofei/CN=v2ray.kkk"

cp templates/nginx.conf /etc/nginx/
cp templates/host.txt /etc/nginx/

# start services
systemctl enable nginx
systemctl enable v2ray
systemctl start nginx
systemctl start v2ray


# install python3
yum install -y python3
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools
python3 -m pip install grpcio requests protobuf uuid


