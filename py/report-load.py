#!/usr/bin/python3
# author: gfw-breaker

import sys, json, uuid, requests, os, random
import api, subprocess, math

apiEndpoint = os.environ.get('FREE_ENDPOINT')
bandwidth = os.environ.get('FREE_BANDWIDTH')
node = sys.argv[1]


if bandwidth is None:
	bandwidth = 1000
else:
	bandwidth = int(bandwidth)


def logFailure(info):
	f = open('/root/phoenix/failure.txt', "w")
	f.write(info)
	f.close()


def getLoad():
	command = "/usr/bin/sar -n DEV 10 1 | grep 'Average:' | grep 'eth0' | awk '{print $6}'"
	status, output = subprocess.getstatusoutput(command)
	print(output)
	print(bandwidth)
	if status != 0:
		raise Error
	outSpeed = math.ceil(float(output))* 8
	avgLoad = outSpeed / (bandwidth* 10) 
	return math.ceil(avgLoad)

#print(getLoad())

authToken = api.getToken()
print("token:" + authToken)
bearer = "Bearer %s" % authToken
url = "%s/ipoint" % apiEndpoint

headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
	"Authorization": bearer
}

payload = {
  "cmd": "load-report",
  "node": node,
  "load": getLoad()
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
	


