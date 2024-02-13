import os
import sys
import requests

URL = "https://api.gandi.net/v5/domain/check"

try:
    apikey = os.environ["GANDI_API"]
except KeyError:
    print("Environment variable GANDI_API must be set.")
    sys.exit(1)

headers = {"authorization": "Apikey " + apikey}

for domain in ("aaa","zzz"):
    print(domain)
sys.exit(0)

querystring = {
    "name": sys.argv[1],
}

try:
    response = requests.request("GET", URL, headers=headers, params=querystring)
    response.raise_for_status()
except Exception as err:
    print(f"Error occurred: {err}")

json_data = response.json()
products = json_data.get("products")
print("{} is {}".format(sys.argv[1], products[0].get("status")))
