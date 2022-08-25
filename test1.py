import serial
import time
import RPi.GPIO as gp

gp.setmode(gp.BCM) # header index: NAME  둘중 무조건 입력하고 시작
# gp.setmode(gp.BOARD) # header index: PIN#
port="/dev/ttyACM0"
serialFromArduino = serial.Serial(port, 9600)
serialFromArduino.flushInput()
input_s = serialFromArduino.readline()
input = str(input_s)
#input = int(input_s)
result = input[2:-5]
print(result)
time.sleep(5)

