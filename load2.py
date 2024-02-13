import string
import time
import sqlite3

dictionary = "american-english-insane"

badchars = string.punctuation + string.whitespace

data=[]
timestamp = time.time()

with open(dictionary) as f:
    for word in f:
        if "'" in word:
            continue
        if len(word.strip(badchars)) == 3:
            data.append((word.strip(badchars),'unknown',timestamp))
                        
database = "domains.db"
con = sqlite3.connect(database)
cur = con.cursor()
cur.executemany("INSERT INTO domains VALUES (?, ?, ?)",data)
con.commit()