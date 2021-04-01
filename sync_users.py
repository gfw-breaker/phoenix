#!/usr/bin/python3
# author: gfw-breaker

import sys, json, uuid, requests
from v2ray_client import Client
from errors import *

conf = '/usr/local/etc/v2ray/config.json'
baseUrl = 'https://enpvlchz2abbrgu.m.pipedream.net'

INBOUND_TAG = 'proxy'
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = '10085'


# main
client = Client(address=SERVER_ADDRESS, port=SERVER_PORT)

response = requests.get(baseUrl)
accounts = response.json()

for account in accounts: 
	email = account['email']
	uuid = account['uuid']
	try:
		client.add_user(inbound_tag=INBOUND_TAG,user_id=uuid,email=email,level=0,alter_id=16)
	except EmailExistsError as e:
		pass


# save to file
with open(conf, 'r') as confFile:
    root = json.load(confFile)
clients = root['inbounds'][0]['settings']['clients']
emails = { c['email'] for c in clients }

for account in accounts: 
	email = account['email']
	uuid = account['uuid']
	if not email in emails:
		client = { "email": email, "id": uuid, "level": 0 }
		clients.append(client)

with open(conf, 'w') as confFile:
    json.dump(root, confFile, indent=2)



