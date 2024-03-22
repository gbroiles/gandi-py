#!/usr/bin/python3

import string
import time
import sqlite3
import sys
import random

dictionary = "american-english-insane"

UNKNOWN = 0
AVAILABLE = 1
UNAVAILABLE = 2

badchars = string.punctuation + string.whitespace

database = "domains.db"
con = sqlite3.connect(database, timeout=180)
cur = con.cursor()

data = []
timestamp = time.time()


def dbload(mydata):
    if random.randint(0, 1000) == 0:
        print("Attempt: ", mydata)
    try:
        cur.execute("INSERT INTO domains VALUES (?, ?, ?)", mydata)
        con.commit()
    except sqlite3.IntegrityError as er:
        print("duplicate: ", mydata)
    except sqlite3.Error as er:
        print("SQLite error: %s" % (" ".join(er.args)))
        print("Exception class is: ", er.__class__)
        print("SQLite traceback: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    return


with open(dictionary) as f:
    for word in f:
        word2 = word.strip(badchars)
        word3 = word2.lower()
        if "'" in word3:
            continue
        for extension in [".com", ".net", ".org"]:
            dbload((word3 + extension, UNKNOWN, timestamp))
