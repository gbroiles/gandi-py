#!/usr/bin/python3

import os
import psutil
import random
import sys
import time
import sqlite3

UNKNOWN = 0
AVAILABLE = 1
UNAVAILABLE = 2
timestamp = time.time()

database = "domains.db"

con = sqlite3.connect(database)
cur = con.cursor()

lines = []

for i in sys.argv[1:]:
    for line in open(i):
        data = (line.strip("\n."), UNAVAILABLE, timestamp)
        cur.execute("REPLACE INTO domains VALUES (?, ?, ?)", data)
        if random.randint(0, 100000) == 0:
            print(
                (time.time() - timestamp),
                ":",
                psutil.Process(os.getpid()).memory_info().rss / 1024**2,
                ":",
                line,
                end="",
            )
            con.commit()
con.commit()
