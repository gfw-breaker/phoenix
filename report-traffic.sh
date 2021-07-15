#!/bin/bash

## v2ray traffic API
_APISERVER=127.0.0.1:10085
_V2CTL=/usr/local/bin/v2ctl

apidata () {
    local ARGS=
    if [[ $1 == "reset" ]]; then
      ARGS="reset: true"
    fi
    $_V2CTL api --server=$_APISERVER StatsService.QueryStats "${ARGS}" \
    | awk '{
        if (match($1, /name:/)) {
            f=1; gsub(/^"|link"$/, "", $2);
            split($2, p,  ">>>");
            printf "%s:%s->%s\t", p[1],p[2],p[4];
        }
        else if (match($1, /value:/) && f){ f = 0; printf "%.0f\n", $2; }
        else if (match($0, /^>$/) && f) { f = 0; print 0; }
    }'
}


## main
source /etc/profile
cd /root/phoenix

apidata reset | grep 'user:' | grep '\->down' | sed -e 's/user://g' -e 's/->down//g' | sed 's/@.*\s/,/g' | grep -v ",0$" > data.txt

lines=$(wc -l data.txt | cut -d' ' -f1)
if [ $lines -eq 0 ]; then
	echo "no traffic data available."
	exit 0
fi

node=$(/usr/sbin/ifconfig eth0 | grep 'inet ' | awk '{print $2}')

/usr/bin/python3 py/report-traffic.py $node


