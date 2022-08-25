import serial
import time
import RPi.GPIO as gp
def data_send():
    gp.setmode(gp.BCM) # header index: NAME  둘중 무조건 입력하고 시작
    # gp.setmode(gp.BOARD) # header index: PIN#
    gp.setup(18,gp.OUT)
    gp.setup(23,gp.OUT)
    gp.setup(24,gp.OUT)
    port="/dev/ttyACM0"
    serialFromArduino = serial.Serial(port, 9600)
    serialFromArduino.flushInput()
    check = True
    cnt = 0
    input_s = serialFromArduino.readline()
    input = str(input_s)
    #input = int(input_s)
    result = input[2:7] + input[8:-5]
    print(result)
    #h= float(input[2:7])
    h= float(input[2:7])
    t= float(input[8:-5])
    time.sleep(1)
    cnt += 1
    if t >= 24:
        gp.output(18, gp.HIGH)
        gp.output(23, gp.LOW)
    elif t<= 10:
        gp.output(18, gp.LOW)
        gp.output(23, gp.HIGH)
    else:
        gp.output(18, gp.LOW)
        gp.output(23, gp.HIGH)
    print(cnt)
    if h <=80:
        cnt = 0
        if check == True:
            gp.output(24, gp.HIGH)
    if cnt == 10:
        check = False
        gp.output(24, gp.LOW)
    return result