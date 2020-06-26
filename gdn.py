#!/usr/bin/python3

import requests


url = "https://api.gandi.net/v5/domain/check"

querystring = {"name":"example.com","processes":["create","transfer"],"grid":"C"}

headers = {'authorization': 'Apikey your-api-key'}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
