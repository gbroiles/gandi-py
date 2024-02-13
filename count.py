import sqlite3

print(sqlite3.connect("domains.db").execute("select count(*) from domains;").fetchall())