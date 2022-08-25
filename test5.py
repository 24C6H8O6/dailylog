from flask import Flask,render_template
import requests
import time
import sen_all
from concurrent.futures import ThreadPoolExecutor
import RPi.GPIO as gp

app = Flask(__name__)

gp.setmode(gp.BCM)
gp.setup(18,gp.OUT)
gp.setup(22,gp.OUT)
gp.setup(23,gp.OUT)

# 수동 제어(html에서 각각의 토글스위치가 on/off되는 것에 <<function fan_on(){fetch('/fan/on')}>> 이런식으로 작성 필요)
@app.route('/auto/off')
def auto_off():
    gp.output(18, gp.LOW)
    gp.output(22, gp.LOW)
    gp.output(23, gp.LOW)
    time.sleep(1)
 # 1. 팬 수동제어
@app.route('/led/on')
def fan_on():
    gp.output(18, gp.HIGH)
@app.route('/led/off')
def fan_off():
    gp.output(18, gp.LOW)
 # 2. 히터 수동제어
@app.route('/heat/on')
def heat_on():
    gp.output(22, gp.HIGH)
@app.route('/heat/off')
def heat_off():
    gp.output(22, gp.LOW)
 # 3. 워터펌프 수동제어
@app.route('/pump/on')
def pump_on():
    gp.output(23, gp.HIGH)
@app.route('/pump/off')
def pump_off():
    gp.output(23, gp.LOW)


# 자동 제어
@app.route('/auto/on')
def auto_on():
    gp.output(18, gp.LOW)
    gp.output(22, gp.LOW)
    gp.output(23, gp.LOW)
    time.sleep(1)
   
# 아두이노에서 받은 센서값 계속 오라클db로 전달
def get_url(url):
    return requests.get(url)
data = sen_all.data_send()
 # temp(온도), hd(습도), lux(조도), waterA(급수), waterD(배수), moi(토양습도) 센서값 띄어쓰기로 분리
temp, hd, lux, waterA, waterD, moi = data.split(' ')
def tes(data):
    list_of_urls = [f"http://192.168.0.4:5011?data={data}"]
    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(get_url,list_of_urls)) 
    for response in response_list:
        print(response)

while True:
    #tes(data)
    time.sleep(1) 
    # 히터 작동
    if float(temp) <= plant_dataset_temp: 
        gp.output(18,gp.HIGH)
    else:
        gp.output(18,gp.LOW)
    # 팬 작동
    if float(hd) >= plant_dataset_hd:
        gp.output(22,gp.HIGH)
    else:
        gp.output(22,gp.LOW)   
    # 급수 탱크(수위 조절)
    if int(waterA) <= 120:
        def add_water(data1):
            data1 = 'Please add water'
            addWater = [f"http://192.168.30.114:5099/test?data={data1}"]
            with ThreadPoolExecutor(max_workers=10) as pool:
                response_list = list(pool.map(get_url,addWater))  
            for response in response_list:
                print(response)
    # 배수 탱크(수위 조절)
    if int(waterD) >= 500:
        def dump_water(data2):
            data2 = 'Please dump water'
            dumpWater = [f"http://192.168.30.114:5099/test?data={data2}"]
            with ThreadPoolExecutor(max_workers=10) as pool:
                response_list = list(pool.map(get_url,dumpWater))  
            for response in response_list:
                print(response)
    # 토양 습도(물주기)
    if int(moi) <= plant_dataset_moi:
        gp.output(23,gp.HIGH)
    else:
        gp.output(23,gp.LOW)
