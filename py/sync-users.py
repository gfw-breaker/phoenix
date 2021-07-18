#!/usr/bin/python3
# author: gfw-breaker

import os, sys, json, requests
import api
from v2ray_client import Client
from errors import *


apiEndpoint = os.environ.get('FREE_ENDPOINT')

conf = '/usr/local/etc/v2ray/config.json'
INBOUND_TAG = 'proxy'
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = '10085'

client = Client(address=SERVER_ADDRESS, port=SERVER_PORT)


def addToConf(uid):
	with open(conf, 'r') as confFile:
		root = json.load(confFile)
	clients = root['inbounds'][0]['settings']['clients']
	emails = { c['email'] for c in clients }

	email = "%s@test.com" % (uid)
	if not email in emails:
		client = { "email": email, "id": uid, "level": 0 }
		clients.append(client)

	with open(conf, 'w') as confFile:
		json.dump(root, confFile, indent=2)


def removeFromConf(uid):
	return


def addUser(uid):
	email = "%s@test.com" % (uid)
	try:
		client.add_user(inbound_tag=INBOUND_TAG,user_id=uid,email=email,level=0,alter_id=16)
	except Exception as e:
		pass
	addToConf(uid)


def removeUser(uid):
	return


## main
url = "%s/ipoint" % apiEndpoint
headers = api.getHeaders()

payload = {
  "cmd": "service-a"
}

try:
	r = requests.post(url, headers=headers, data=json.dumps(payload))
	if r.status_code != 200:
		print('failed')
		sys.exit(1)
except Exception as e:
	print('failed')
	sys.exit(2)

print(r.json())
uidList = r.json()['data']

for uid in uidList:
	addUser(uid)



