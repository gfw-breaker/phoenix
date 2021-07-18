#!/usr/bin/python3
# author: gfw-breaker

import sys, json, uuid, requests, os
import api

apiEndpoint = os.environ.get('FREE_ENDPOINT')
fastFlag = os.environ.get('FREE_FASTNODE')

node = api.getNodeMd5(sys.argv[1])


def getUserData():
	dataMap = {}
	dataFile = open('/root/phoenix/data.txt', "r")
	for line in dataFile.readlines():
		cols = line.rstrip().split(",")
		dataMap[cols[0]] = int(cols[1])
	return dataMap


def logFailure(info):
	f = open('/root/phoenix/failure.txt', "w")
	f.write(info)
	f.close()


def isFast():
	return fastFlag.lower() in ("yes", "true")


## main
url = "%s/ipoint" % apiEndpoint
headers = api.getHeaders()

payload = {
  "cmd": "data-report",
  "node": node,
  "fast": isFast(),
  "data": getUserData()
}

print(payload)

try:
	r = requests.post(url, headers=headers, data=json.dumps(payload))
	print(r.json())
	status = r.json().get('suc', False)

	if not status:
		logFailure("API gateway error: ipoint")
		sys.exit(1)
except Exception as e:
	print("ok")
	logFailure(str(e))
	sys.exit(2)
	


