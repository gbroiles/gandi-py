#!/usr/bin/python3

import datetime
import os
import string
import sys
import time
import random
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
    print(now, file=sys.stderr, end="")
    print(" - ", file=sys.stderr, end="")
    print(output, file=sys.stderr, flush=True)


try:
    apikey = os.environ["GANDI_API"]
except KeyError:
    print("Environment variable GANDI_API must be set.")
    sys.exit(1)

headers = {"authorization": "Apikey " + apikey}

DELAYMAX = 60
TIMEOUT = 60
SEARCHTARGET = "______.___"

database = "domains.db"
con = sqlite3.connect(database, timeout=TIMEOUT)
debugprint("Database connection successful.")
cur = con.cursor()
con.row_factory = sqlite3.Row
res = con.execute(
    "SELECT * FROM domains WHERE STATUS = "
    + str(UNKNOWN)
    + " AND NAME LIKE '"
    + SEARCHTARGET
    + "';"
)
debugprint("Got result list")
all = res.fetchall()
for row in all:
    name = row[0]
    status = row[1]
    timestamp = row[2]
    querystring = {"name": name}
    try:
        response = requests.request("GET", URL, headers=headers, params=querystring)
        response.raise_for_status()
    except Exception as err:
        debugprint(f"Fetch error occurred: {err} on {name}")
        continue
    try:
        json_data = response.json()
        products = json_data.get("products")
        new_status = products[0].get("status")
        debugprint(name + " " + str(new_status))
        if new_status == "available":
            update_status = AVAILABLE
        elif new_status == "unavailable":
            update_status = UNAVAILABLE
        else:
            update_status = UNKNOWN
        mytuple = (name, update_status, time.time())
    except TypeError:
        mytuple = (name, UNKNOWN, time.time())
    except:
        type, value, tb = sys.exc_info()
        pprint.pprint(type, file=sys.stderr)
        debugprint(
            "\n" + "".join(traceback.format_exception(type, value, tb)).strip("\n")
        )
        continue
    cur.execute("REPLACE INTO domains(name, status, date) VALUES (?, ?, ?)", mytuple)
    con.commit()
    time.sleep(random.uniform(0, DELAYMAX))
