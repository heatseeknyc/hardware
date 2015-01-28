import logging; logging.basicConfig(level=logging.INFO)
import time

import requests

from . import common


READINGS_URI = 'http://hubs.heatseeknyc.com/readings'


def transmit(db):
    for reading_id, cell_id, timestamp, temperature in db.get_untransmitted_readings():
        data = dict(hub=common.PI_ID, cell=cell_id, time=timestamp, temp=temperature)
        logging.info('PATCHing {}'.format(data))
        requests.patch(READINGS_URI, data)
        time.sleep(1)

@common.forever
def main():
    db = common.Database()
    logging.info('connected to database.')
    while True:
        transmit(db)
        time.sleep(1)

if __name__ == '__main__':
    logging.info('starting...')
    main()
