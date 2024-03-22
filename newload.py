#!/usr/bin/python3

import time
import sys
import traceback
import sqlite3

database = "domains.db"

con = sqlite3.connect(database)

cur = con.cursor()

data = []

def dbload(cur, con, mydata):
    try:
        cur.execute("INSERT INTO domains VALUES (?, ?, ?)",(name+".com",'unknown',timestamp))
        con.commit()
    except sqlite3.IntegrityError as er:
        print("duplicate: ",mydata)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    return

for num in range(0,10000):
    name=str(num)
    timestamp=time.time()
    dbload(cur, con, (name+".com",'unknown',timestamp))
    dbload(cur, con, (name+".net",'unknown',timestamp))
    dbload(cur, con, (name+".org",'unknown',timestamp))
print("finished!")
con.commit()

