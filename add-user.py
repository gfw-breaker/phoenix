#!/usr/bin/python
# author: gfw-breaker


import sys, json, uuid

email = sys.argv[1]

conf = '/usr/local/etc/v2ray/config.json'
with open(conf, 'r') as confFile:
    root = json.load(confFile)
clients = root['inbounds'][0]['settings']['clients']


# check whether user exists
for client in clients:
    if client['email'] == email:
        print "User:%s already exists" % email
        sys.exit(0)


# add client to config file
userId = str(uuid.uuid1())
client = { "email": email, "id": userId, "level": 0 }
clients.append(client)
with open(conf, 'w') as confFile:
    json.dump(root, confFile, indent=2)


print "User:%s added" % email


