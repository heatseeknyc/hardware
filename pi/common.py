import sqlite3
import time

class Database:
    def __init__(self):
        self.db = sqlite3.connect('temperatures.db')
        self.db.cursor().execute('create table if not exists temperatures'
                                 ' (xbee, time, temperature)')
        self.db.commit()

    def insert(self, xbee, temperature):
        self.db.cursor().execute('insert into temperatures values (?, ?, ?)',
                               (xbee, round(time.time()), temperature))
        self.db.commit()
