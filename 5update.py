#!/usr/bin/python3

import datetime
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

def debugprint(output):
    now = datetime.datetime.now().strftime("%H:%M:%S.%f")
    print(now + " -- " + output, file=sys.stderr, flush=True)

try:
    apikey = os.environ["GANDI_API"]
except KeyError:
    print("Environment variable GANDI_API must be set.")
    sys.exit(1)

headers = {"authorization": "Apikey " + apikey}

DELAY = 5
TIMEOUT = 60

updatelist=[]

database = "domains.db"
con = sqlite3.connect(database, timeout=TIMEOUT)
debugprint("Database connection successful.")
cur = con.cursor()
con.row_factory = sqlite3.Row
#res = con.execute("SELECT * FROM domains WHERE STATUS = "+str(UNKNOWN)+" AND NAME LIKE '____.___' LIMIT 20;")
res = con.execute("SELECT * FROM domains WHERE STATUS = "+str(UNKNOWN)+" AND NAME LIKE '____.___';")
debugprint("Got result list")
all = res.fetchall()
#pprint.pprint(all)
for row in all:
    name = row[0]
    status = row[1]
    timestamp = row[2]
#    debugprint(name+" "+str(status)+" "+str(timestamp))
#    continue
    querystring = {"name":name}
#    print(name,file=sys.stderr)
    try:
#        debugprint(f"requesting {querystring}")
        response = requests.request("GET", URL, headers=headers, params=querystring)
        response.raise_for_status()
    except Exception as err:
        debugprint(f"Fetch error occurred: {err} on {name}")
        continue
#    debugprint(response.text)
    try:
#        debugprint("inside the try!")
        json_data = response.json()
        products = json_data.get("products")
        new_status = products[0].get("status")
        debugprint(name+" "+str(new_status))
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
        pprint.pprint(type, file=sys.stderr)
        debugprint("\n" + ''.join(traceback.format_exception(type, value, tb)).strip("\n"))
        continue
#    debugprint(str(mytuple)+" about to REPLACE")
    cur.execute("REPLACE INTO domains VALUES (?, ?, ?)",mytuple)
    con.commit()
#    debugprint("did it!"+str(mytuple))
    time.sleep(DELAY)
