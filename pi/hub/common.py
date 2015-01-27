import functools
import logging
import sqlite3
import time


def forever(f):
    @functools.wraps(f)
    def g(*args, **kwargs):
        while True:
            try:
                f(*args, **kwargs)
            except Exception:
                logging.exception('error, retrying...')
                time.sleep(1)
    return g


class Database:
    def __init__(self):
        self.db = sqlite3.connect('heatseeknyc.db')
        self.db.execute('create table if not exists temperatures (xbee, time, temperature)')
        self.db.execute('create table if not exists transmitted as select 0 as temperature_id')

    def insert_temperature(self, xbee, temperature):
        with self.db as db:
            db.execute('insert into temperatures values (?, ?, ?)',
                       (xbee, round(time.time()), temperature))

    def get_untransmitted_temperatures(self):
        with self.db as db:
            (temperature_id,), = db.execute('select temperature_id from transmitted')
            return db.execute('select rowid, * from temperatures where rowid > ?', temperature_id)

    def set_transmitted_temperatures(self, temperature_id):
        with self.db as db:
            db.execute('update transmitted set temperature_id = ?', temperature_id)
