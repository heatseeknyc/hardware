import binascii
import logging
logging.basicConfig(level=logging.INFO)
from struct import Struct
import time

import pylibftdi
pylibftdi.driver.USB_PID_LIST.append(0x6015)

SHORT = Struct('>H') # big endian unsigned short

def read(f, length):
    s = b''
    while True:
        s += f.read(length - len(s))
        if len(s) == length: break
        time.sleep(0.01)
    return s

def read_sensor(xbee):
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

        voltage = adc / 0x3FF * 1.2 # on Xbee, 0x3FF (highest value on a 10-bit ADC) corresponds to 1.2V
        celsius = 25 + (voltage - 0.75) / 0.01 # on TMP36, 0.75V is 25C, and every 0.01V difference is 1C difference
        fahrenheit = celsius * (212 - 32) / 100 + 32
        
        sensor_global_id = binascii.hexlify(sensor_global_id).decode('ascii')

        signature = 'c0ffee' # TODO actually sign row using a secret key

        print('{}\t{}\t{}\t{}'
              .format(int(time.time()), sensor_global_id, int(fahrenheit), signature))

def main():
    logging.info('attempting connection to ftdi usb...')
    with pylibftdi.Device() as xbee: # defaults to 9600/8N1
        logging.info('...connected')
        while True:
            try:
                read_sensor(xbee)
            except Exception:
                logging.exception("failed to read a packet")

if __name__ == '__main__':
    main()
