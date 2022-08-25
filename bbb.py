import RPi.GPIO as gp

gp.setwarnings(False)
gp.setmode(gp.BCM)
gp.setup(18,gp.OUT)

while True:
    gp.output(18,1)
    