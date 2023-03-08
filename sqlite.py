#used to create the database

import sqlite3

conn = sqlite3.connect('test.db')

conn.execute(
'''
CREATE TABLE test
(id INTEGER PRIMARY KEY, username TEXT, password TEXT)
'''
)

conn.commit()
conn.close()