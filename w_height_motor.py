import serial
import time
import RPi.GPIO as gp
gp.setmode(gp.BCM)
gp.setup(17, gp.OUT)
port = '/dev/ttyACM0'
serialFromArduino = serial.Serial(port, 9600)
serialFromArduino.flushInput()
input_s = serialFromArduino.readline()
input = str(input_s)
print(input[2:-5])
moi = int(input[2:-5])
#a = 1
"""while a:
    if seri.in_waiting != 0 :
        content = seri.readline()
        #print(content.decode())
        a = content[:-2].decode()
        print(a)
        moi = a
"""
if moi <= 50:  # send warning message to server
    gp.output(17, gp.HIGH)