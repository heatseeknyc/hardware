import binascii
import logging
logging.basicConfig(level=logging.INFO)
import os
from struct import Struct
import time

import serial

SHORT = Struct('>H') # big endian unsigned short


def read_sensor(xbee):
    frame_start, = xbee.read()
    if frame_start != 0x7E:
        raise Exception('expected frame start byte 0x7E but got {:02X}'.format(frame_start))

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
        sensor_global_id = frame[1:1+8]
        adc, = SHORT.unpack(frame[16:16+2])

        voltage = adc / 0x3FF * 1.2
        celsius = 25 + (voltage - 0.75) / 0.01
        fahrenheit = celsius * (212 - 32) / 100 + 32
        
        sensor_global_id = binascii.hexlify(sensor_global_id).decode('ascii')
        print('{},{},{}'.format(int(time.time()), sensor_global_id, fahrenheit))

def main():
    devs = os.listdir('/dev/')
    usbserials = [dev for dev in devs if dev.startswith('tty.usbserial')]
    if not usbserials:
        logging.error('no /dev/tty.usbserial* device found; is the ftdi driver installed and the xbee usb dongle plugged in?')
        return
    logging.info('connecting to {}...'.format(usbserials[0]))
    with serial.Serial('/dev/' + usbserials[0]) as xbee: # defaults to 9600/8N1
        logging.info('...connected to {}'.format(xbee.name))
        while True:
            read_sensor(xbee)


if __name__ == '__main__':
    main()
