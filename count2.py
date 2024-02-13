import sqlite3

print(sqlite3.connect("domains.db").execute("select count(*) from domains where status is 'failed';").fetchall())
