#!/usr/bin/python3
# author: gfw-breaker

import os, sys, json, uuid, requests
import api


apiEndpoint = os.environ.get('FREE_ENDPOINT')


## main
authToken = api.getToken()
bearer = "Bearer %s" % authToken
url = "%s/ipoint" % apiEndpoint

headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
	"Authorization": bearer
}

payload = {
  "cmd": "domain"
}

try:
	r = requests.post(url, headers=headers, data=json.dumps(payload))
	if r.status_code != 200:
		print('failed')
		sys.exit(1)
except Exception as e:
	print('failed')
	sys.exit(2)

#print(r.json())

for item in r.json()['data']:
	path = item['path']
	domain = item['domain']
	record = 'mapping:%s:%s' % (path, domain)
	print(record)





