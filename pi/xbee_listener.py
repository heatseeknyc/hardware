import binascii
import logging
logging.basicConfig(level=logging.INFO)
import serial
from struct import Struct
import time

from . import database

SHORT = Struct('>H') # big endian unsigned short

def read(f, length):
    s = b''
    while True:
        s += f.read(length - len(s))
        if len(s) == length: break
        time.sleep(0.01)
    return s

def read_sensor(xbee, db):
    frame_start, = read(xbee, 1)
    if frame_start != 0x7E:
        raise Exception('expected frame start byte 0x7E but got {:02X}'.format(frame_start))

    length, = SHORT.unpack(read(xbee, 2))

    frame = read(xbee, length + 1) # frame plus checksum byte

    checksum = 0
    for byte in frame:
        checksum = (checksum + byte) & 0xFF
    if checksum != 0xFF:
        raise Exception('expected frame plus checksum to be 0xFF but got {:02X}'.format(checksum))

    if frame[0] == 0x92: # IO Data Sample RX
        if length != 18:
            raise Exception('expected length of 18 for 0x92 frame, but got {}'.format(length))
        sensor_global_id = frame[1:1+8]
        adc, = SHORT.unpack(frame[16:16+2])

        voltage = adc / 0x3FF * 3.3 # on Xbee, 0x3FF (highest value on a 10-bit ADC) corresponds to VCC...ish
        celsius = (voltage - 0.5) / 0.01 # on MCP9700A, 0.5V is 0C, and every 0.01V difference is 1C difference
        fahrenheit = celsius * (212 - 32) / 100 + 32

        logging.info('adc=0x{:x} voltage={:.2f} celsius={:.2f} fahrenheit={:.2f}'.format(adc, voltage, celsius, fahrenheit))
        
        sensor_global_id = binascii.hexlify(sensor_global_id).decode('ascii')

        db.insert(sensor_global_id, round(fahrenheit, 2))


def main():
    xbee = serial.Serial('/dev/ttyAMA0') # defaults to 9600/8N1
    db = database.Database()
    while True:
        try:
            read_sensor(xbee, db)
        except Exception:
            logging.exception("failed to read a packet")

if __name__ == '__main__':
    main()
