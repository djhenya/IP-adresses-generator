#!/usr/bin/python

import sqlite3 as sqlite

con = sqlite.connect('test.db')

cur = con.cursor()

#cur.execute("create table test (col1 varchar(255), col2 varchar(255), Primary key(col1))")

cur.execute('insert into test values ("254", "helloworld1")')
print cur.execute('select * from test').fetchall()

con.commit()