import os
import string
import sys
import time
import requests

URL = "https://api.gandi.net/v5/domain/check"

try:
    apikey = os.environ["GANDI_API"]
except KeyError:
    print("Environment variable GANDI_API must be set.")
    sys.exit(1)

headers = {"authorization": "Apikey " + apikey}

delay = 0.3
dictionary = "american-english-insane"

badchars = string.punctuation + string.whitespace

mylist = []

with open(dictionary) as f:
    for word in f:
        if "'" in word:
            continue
        if len(word.strip(badchars)) == 3:
            mylist.append(word.strip(badchars))

size = len(mylist)
print(str(size * delay / 60) + " minutes", file=sys.stderr)

for domain in mylist:
    querystring = {"name": domain + ".com"}
    try:
        response = requests.request("GET", URL, headers=headers, params=querystring)
        response.raise_for_status()
    except Exception as err:
        print(f"Error occurred: {err}")
    json_data = response.json()
    #    print(json_data)
    products = json_data.get("products")
    print(
        "{} is {}".format(products[0].get("name"), products[0].get("status")),
        file=sys.stderr,
    )
    if products[0].get("status") != "unavailable":
        print(products[0].get("name"))
    time.sleep(1)
