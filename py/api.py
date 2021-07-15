#!/usr/bin/python3
# author: gfw-breaker

import sys, json, uuid, requests, os

identifier = os.environ.get('FREE_IDENTIFIER')
password = os.environ.get('FREE_PASSWORD')
apiEndpoint = os.environ.get('FREE_ENDPOINT')


url = "%s/vlogin" % apiEndpoint
headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
}

payload = {
	"identifier": identifier,
	"password": password
}


def getToken():
	r = requests.post(url, headers=headers, data=json.dumps(payload))
	if r.status_code == 400:
		raise Exception('API Gateway error: vlogin')
	token = r.json()['token']
	#print(token)
	return token



