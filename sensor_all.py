import serial
import time
import RPi.GPIO as gp
def data_send():
    port="/dev/ttyACM0"
    serialFromArduino = serial.Serial(port, 9600)
    serialFromArduino.flushInput()
    input_s = serialFromArduino.readline()
    data = str(input_s)
    # 온도,습도,조도,토양수분,급수,배수 순으로
    temp = float(data[])
    hd = float(data[])
    light = float(data[])
    soil_moi = float(data[])
    water_su = float(data[])
    water_dr = float(data[])
    time.sleep(1)
    return data[2:-5]
    