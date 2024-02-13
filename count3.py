import sqlite3

print(sqlite3.connect("domains.db").execute("select count(*) from domains where status is 'failed';").fetchall()," failed")
print(sqlite3.connect("domains.db").execute("select count(*) from domains where status is 'available';").fetchall()," available")
print(sqlite3.connect("domains.db").execute("select count(*) from domains where status is 'unavailable';").fetchall()," unavailable")
print(sqlite3.connect("domains.db").execute("select count(*) from domains where status is 'unknown';").fetchall()," unknown")
