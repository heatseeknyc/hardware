import binascii
import logging; logging.basicConfig(level=logging.INFO)
from struct import Struct

import serial

from . import common


SHORT = Struct('>H') # big endian unsigned short

def listen(xbee, db):
    while xbee.read(1) != b'\x7E':
        logging.warn('expected frame start byte 0x7E but got {:02X}'.format(frame_start))

    length, = SHORT.unpack(xbee.read(2))

    frame = xbee.read(length + 1) # frame plus checksum byte

    checksum = 0
    for byte in frame:
        checksum = (checksum + byte) & 0xFF
    if checksum != 0xFF:
        raise Exception('expected frame plus checksum to be 0xFF but got {:02X}'.format(checksum))

    if frame[0] == 0x92: # IO Data Sample RX
        if length != 18:
            raise Exception('expected length of 18 for 0x92 frame, but got {}'.format(length))
        cell_id = frame[1:1+8]
        adc, = SHORT.unpack(frame[16:16+2])

        cell_id = binascii.hexlify(cell_id).decode('ascii')

        voltage = adc / 0x3FF * 3.3 # on Xbee, 0x3FF (highest value on a 10-bit ADC) corresponds to VCC...ish
        celsius = (voltage - 0.5) / 0.01 # on MCP9700A, 0.5V is 0C, and every 0.01V difference is 1C difference
        fahrenheit = celsius * (212 - 32) / 100 + 32

        logging.info('cell_id={} adc=0x{:x} voltage={:.2f} celsius={:.2f} fahrenheit={:.2f}'.format(cell_id, adc, voltage, celsius, fahrenheit))

        # our resolution ends up being about 0.6F, so we round to 1 digit:
        db.insert_reading(cell_id, round(fahrenheit, 1))

@common.forever
def main():
    db = common.Database()
    logging.info('connected to database.')
    with serial.Serial('/dev/ttyAMA0') as xbee:
        logging.info('connected to xbee.')
        while True:
            listen(xbee, db)

if __name__ == '__main__':
    logging.info('starting...')
    main()
