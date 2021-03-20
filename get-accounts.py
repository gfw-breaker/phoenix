#!/usr/bin/python
# author: gfw-breaker


import sys, json, uuid
import requests

baseUrl = 'https://enpvlchz2abbrgu.m.pipedream.net'

response = requests.get(baseUrl)


accounts = response.json()

for account in accounts: 
	email = account['email']
	uuid = account['uuid']
	print email, uuid


