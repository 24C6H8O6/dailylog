import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)
gp.setup(18,gp.OUT)
gp.setup(22,gp.OUT)
gp.setup(23,gp.OUT)

gp.output(18, gp.HIGH)
gp.output(22, gp.HIGH)
gp.output(23, gp.HIGH)

