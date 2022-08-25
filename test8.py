import requests
import time
import sen_all
from concurrent.futures import ThreadPoolExecutor
import RPi.GPIO as gp

gp.setmode(gp.BCM)
gp.setup(17,gp.OUT)
gp.setup(18,gp.OUT)
gp.setup(22,gp.OUT)
gp.setup(23,gp.OUT)
gp.setup(24,gp.OUT)
gp.setup(25,gp.OUT)

def get_url(url):
    return requests.get(url)
while True:
    data = sen_all.data_send()
    temp, hd, lux, waterA, waterD, moi = data.split(' ')
    print(temp)