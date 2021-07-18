#!/usr/bin/python3

import sys, json, uuid, requests, os, hashlib


identifier = os.environ.get('FREE_IDENTIFIER')
password = os.environ.get('FREE_PASSWORD')
apiEndpoint = os.environ.get('FREE_ENDPOINT')
apiToken = os.environ.get('FREE_API_TOKEN')


url = "%s/vlogin" % apiEndpoint
headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
}

payload = {
	"identifier": identifier,
	"password": password
}


def getHeaders():
	bearer = "Bearer %s" % apiToken
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": bearer
	}
	return headers


def generateToken():
	r = requests.post(url, headers=headers, data=json.dumps(payload))
	if r.status_code == 400:
		raise Exception('API Gateway error: vlogin')
	token = r.json()['token']
	return token


def getNodeMd5(ip):
	return hashlib.md5(ip.encode("utf-8")).hexdigest()


## main
if __name__ == '__main__':
	print(generateToken())


