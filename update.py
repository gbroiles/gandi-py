import os
import string
import sys
import time
import requests
import sqlite3
import pprint
import traceback

URL = "https://api.gandi.net/v5/domain/check"

try:
    apikey = os.environ["GANDI_API"]
except KeyError:
    print("Environment variable GANDI_API must be set.")
    sys.exit(1)

headers = {"authorization": "Apikey " + apikey}

delay = .3

updatelist=[]

database = "domains.db"
con = sqlite3.connect(database)
con.row_factory = sqlite3.Row
res = con.execute("SELECT * FROM domains WHERE STATUS is 'unknown' LIMIT 100;")
for row in res.fetchall():
    name = row[0]
    status = row[1]
    timestamp = row[2]
    querystring = {"name":name}
    print(name,file=sys.stderr)
    try:
#        print(f"requesting {querystring}")
        response = requests.request("GET", URL, headers=headers, params=querystring)
        response.raise_for_status()
    except Exception as err:
        print(f"Fetch error occurred: {err} on {name}")
        continue
#    print(response.text)
    try:
        json_data = response.json()
        products = json_data.get("products")
        new_status = products[0].get("status")
#        print(name,new_status)
        mytuple=(name,new_status,time.time())
    except TypeError:
        mytuple=(name,"failed",time.time())
    except:
        type, value, tb = sys.exc_info()
        pprint.pprint(type)
        print("\n" + ''.join(traceback.format_exception(type, value, tb)).strip("\n"))

    updatelist.append(mytuple)
#    print(mytuple)
    time.sleep(delay)

for item in updatelist:
    print(item)

cur = con.cursor()
cur.executemany("REPLACE INTO domains VALUES (?, ?, ?)",updatelist)
con.commit()