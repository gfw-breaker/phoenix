#!/bin/bash
# author: gfw-breaker(翻墙教练)

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
sed "s/#uuid#/$uuid/g" config.tmp > config.json
cp -f config.json $config_dir


# start service
systemctl start v2ray


