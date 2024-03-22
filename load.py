import time
import sqlite3

database = "domains.db"

con = sqlite3.connect(database)

cur = con.cursor()

data = []

for num in range(0, 10000):
    name = str(num)
    timestamp = time.time()
    data.append((name + ".com", "unknown", timestamp))
    data.append((name + ".net", "unknown", timestamp))
    data.append((name + ".org", "unknown", timestamp))

# for item in data:
#    print(item)

cur.executemany("INSERT INTO domains VALUES (?, ?, ?)", data)
con.commit()
