#!/bin/bash

source /etc/profile
cd /root/phoenix

sed -i '/FREE_API_TOKEN/d' /etc/profile 

token=$(python3 py/api.py)

echo "export FREE_API_TOKEN='$token'" >> /etc/profile




