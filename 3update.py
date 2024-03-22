#!/usr/bin/python3

import os
import string
import sys
import time
import requests
import sqlite3
import pprint
import traceback

UNKNOWN = 0
AVAILABLE = 1
UNAVAILABLE = 2

URL = "https://api.gandi.net/v5/domain/check"

try:
    apikey = os.environ["GANDI_API"]
except KeyError:
    print("Environment variable GANDI_API must be set.")
    sys.exit(1)

headers = {"authorization": "Apikey " + apikey}

delay = 1

updatelist=[]

database = "domains.db"
con = sqlite3.connect(database, timeout=10)
cur = con.cursor()
con.row_factory = sqlite3.Row
res = con.execute("SELECT * FROM domains WHERE STATUS = "+str(UNKNOWN)+" LIMIT 20;")
for row in res.fetchall():
    name = row[0]
    status = row[1]
    timestamp = row[2]
    print(name, status, timestamp)
#    continue
    querystring = {"name":name}
#    print(name,file=sys.stderr)
    try:
        print(f"requesting {querystring}")
        response = requests.request("GET", URL, headers=headers, params=querystring)
        response.raise_for_status()
    except Exception as err:
        print(f"Fetch error occurred: {err} on {name}")
        continue
    print(response.text)
    try:
        print("inside the try!")
        json_data = response.json()
        products = json_data.get("products")
        new_status = products[0].get("status")
        print(name,new_status)
        if new_status == "available":
            update_status = AVAILABLE
        elif new_status == "unavailable":
            update_status = UNAVAILABLE
        else:
            update_status = UNKNOWN
        mytuple=(name,update_status,time.time())
    except TypeError:
        mytuple=(name,UNKNOWN,time.time())
    except:
        type, value, tb = sys.exc_info()
        pprint.pprint(type)
        print("\n" + ''.join(traceback.format_exception(type, value, tb)).strip("\n"))
        continue
    print(mytuple," about to REPLACE")
    cur.execute("REPLACE INTO domains VALUES (?, ?, ?)",mytuple)
    con.commit()
    print("did it!", mytuple)
    time.sleep(delay)
