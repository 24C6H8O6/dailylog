import RPi.GPIO as gp

import time
import sys

sys.path.append('/home/pi/pyFirmata')
import pyfirmata

board=pyfirmata.Arduino('/dev/ttyACM0')

pin13 = board.get_pin('d:13:o')

neoPixel = 'off'
try:
    for i in range(10):
        if neoPixel == 'on':
            pin13.write(1)
            time.sleep(10)
            pin13.write(0)
            time.sleep(0)
        elif neoPixel == 'off':
            pin13.write(1)
            time.sleep(0)
            pin13.write(0)
            time.sleep(10)       
except KeyboardInterrupt:
    gp.cleanup()

'''try:
    while True:
        pin6.write(1)
        time.sleep(10)
        pin6.write(0)
        time.sleep(0)
        
except KeyboardInterrupt:
    gp.cleanup()'''