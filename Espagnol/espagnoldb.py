import sqlite3

conn = sqlite3.connect("espagnol.db")
cursor = conn.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS vocabulaire (id INTEGER PRIMARY KEY AUTOINCREMENT, espagnol TEXT, français TEXT)''')

conn.commit()
conn.close()