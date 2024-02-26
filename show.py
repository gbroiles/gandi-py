import sqlite3

conn = sqlite3.connect("domains.db")

result = conn.execute("select * from domains where status is 'available';").fetchall()

for entry in result:
    print(entry[0])
