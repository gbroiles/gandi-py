import time
import sqlite3


def char_range(c1, c2):
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)


database = "domains.db"

con = sqlite3.connect(database)

cur = con.cursor()

data = []

for c1 in char_range("a", "z"):
    for c2 in char_range("a", "z"):
        for c3 in char_range("a", "z"):
            for c4 in char_range("a", "z"):
                name = c1 + c2 + c3 + c4
                timestamp = time.time()
                data.append((name + ".com", "unknown", timestamp))
                data.append((name + ".net", "unknown", timestamp))
                data.append((name + ".org", "unknown", timestamp))

# for item in data:
#    print(item)

cur.executemany("INSERT INTO domains VALUES (?, ?, ?)", data)
con.commit()
