import functools
import logging
import re
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
        self.db.execute('create table if not exists readings (xbee, time, temperature)')
        self.db.execute('create table if not exists transmitted as select 0 as reading_id')

    def insert_reading(self, xbee, temperature):
        with self.db as db:
            db.execute('insert into readings values (?, ?, ?)',
                       (xbee, round(time.time()), temperature))

    def get_untransmitted_readings(self):
        with self.db as db:
            (reading_id,), = db.execute('select reading_id from transmitted')
            return db.execute('select rowid, * from readings where rowid > ?', reading_id)

    def set_transmitted_readings(self, reading_id):
        with self.db as db:
            db.execute('update transmitted set reading_id = ?', reading_id)

_PI_ID_RE = re.compile('^Serial\s*: (\w*)')
def _get_pi_id():
    with open('/proc/cpuinfo') as f:
        for line in f:
            groups = _PI_ID_RE.findall(line)
            if groups: return group[1]
PI_ID = _get_pi_id() or 'unknown'
