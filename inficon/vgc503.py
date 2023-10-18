import serial
from threading import Thread
import time
import datetime
import csv


"""
running this creates a data.csv file in the same directory which is updated every 0.1s.
 - make sure usbdevice has the right COM port
 - factory default baud rate for gauge control is 115200
"""

usbdevice = 'COM3'
# usbdevice = '/dev/tty3'
baud = 115200
ser = serial.Serial(usbdevice, baud)


# rows are formatted as b'[channel],[data],[channel],[data],[channel],[data]'
def parserow(row: bytes):
    split = row.split(b',')
    strs = list(map(lambda bytes: bytes.decode(), split))  # want to store in file as strings
    return [strs[1], strs[3], strs[5]]

def addrow(row):
    with open('data.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

# breaks buffer into complete lines and incomplete leftovers
def handle_buffer(buffer: bytes):
    l = buffer.split(b'\r\n')
    if len(l) == 1:
        return l, b''
    else:
        return l[:-1], l[-1]

# gets available serial data every 0.1s and writes to csv whenever a full line is ready
def receiving(ser):
    buffer = b''

    while True:
        time.sleep(0.1)
        buffer += ser.read(ser.inWaiting())
        if b'\r\n' in buffer:
            print('buffer')
            print(buffer)

            rows, leftover = handle_buffer(buffer)
            parsedrows = list(map(lambda row: [str(datetime.datetime.now())] + parserow(row), rows))
            buffer = leftover

            print('parsed')
            print(parsedrows)
            for r in parsedrows:
                addrow(r)

Thread(target=receiving, args=(ser,)).start()

# time.sleep(10)
# print('hola')
