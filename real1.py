from flask import Flask,render_template,redirect,request
import requests
from multiprocessing import Process
import time
import sen_all
from concurrent.futures import ThreadPoolExecutor
import RPi.GPIO as gp
import pandas as pd

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

# 1. 히터(18),팬(22),물펌프(23) GPIO 값 설정
gp.setmode(gp.BCM)
gp.setup(18,gp.OUT)
gp.setup(22,gp.OUT)
gp.setup(23,gp.OUT)

# 2. temp(온도), hd(습도), lux(조도), waterA(급수), waterD(배수), moi(토양습도) 센서값 띄어쓰기로 분리
# 아두이노에서 받은 센서값 계속 오라클db로 전달
def get_url(url):
    return requests.get(url)
data = sen_all.data_send()
temp, hd, lux, waterA, waterD, moi = data.split(' ')
def tes(data):
    list_of_urls = [f"http://192.168.70.104:8088?data={data}"]
    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(get_url,list_of_urls)) 
    for response in response_list:
        print(response)
pro1 = Process(args=(data), target=tes)
pro1.start()

# 급수 탱크(수위 조절)
if int(waterA) <= 120:
    def add_water(data1):
        data1 = 'Please add water'
        addWater = [f"http://192.168.70.104:8088/?data={data1}"]
        with ThreadPoolExecutor(max_workers=10) as pool:
            response_list = list(pool.map(get_url,addWater))  
        for response in response_list:
            print(response)
    '''@app.route('/', methods=['GET','POST'])
    def add_water():
        value = "Please add water"
        return render_template('index.html', value=value)'''
    
# 배수 탱크(수위 조절)
if int(waterD) >= 500:
    def dump_water(data2):
        data2 = 'Please dump water'
        dumpWater = [f"http://192.168.70.104:8088/?data={data2}"]
        with ThreadPoolExecutor(max_workers=10) as pool:
            response_list = list(pool.map(get_url,dumpWater))  
        for response in response_list:
            print(response)
    '''@app.route('/', methods=['GET','POST'])
    def dump_water():
        value = "Please dump water"
        return render_template('index.html', value=value)'''

# 3-1. 수동 제어(html에서 각각의 토글스위치가 on/off되는 것에 <<function fan_on(){fetch('/fan/on')}>> 이런식으로 작성 필요)
@app.route('/auto/off')
def auto_off():
    gp.output(18, gp.LOW)
    gp.output(22, gp.LOW)
    gp.output(23, gp.LOW)
    time.sleep(1)
 # 1) 히터 수동제어
@app.route('/heat/on')
def heat_on():
    gp.output(18, gp.HIGH)
@app.route('/heat/off')
def heat_off():
    gp.output(18, gp.LOW)
 # 2) 팬 수동제어
@app.route('/fan/on')
def fan_on():
    gp.output(22, gp.HIGH)
@app.route('/fan/off')
def fan_off():
    gp.output(22, gp.LOW)
 # 3) 워터펌프 수동제어
@app.route('/pump/on')
def pump_on():
    gp.output(23, gp.HIGH)
@app.route('/pump/off')
def pump_off():
    gp.output(23, gp.LOW)

# 자동제어에서는 데이터베이스에서 plant_dataset_temp, plant_dataset_hd, plant_dataset_moi값을 요청해
# 받아와서 제어

# gardenAll 데이터 불러오기
plant_data = pd.read_csv("gardenAll.csv", encoding="euc-kr")
# web에서 라즈베리파이 플라스크로 보내주는 식물 이름을 plant 변수에 저장하여 각각의 데이터 뽑기
# custom 데이터 보내줄 시 각각의 값을 변수에 저장하여 자동 제어
plant_dataset_temp = plant_data[plant_data['temp(°C)']]
plant_dataset_hd = plant_data[plant_data['hd(%)']]
plant_dataset_moi = plant_data[plant_data['water']]
# 3-2. 자동 제어
@app.route('/auto/on')
def auto_on():
    gp.output(18, gp.LOW)
    gp.output(22, gp.LOW)
    gp.output(23, gp.LOW)
    time.sleep(1)

while True:
    #tes(data)
    time.sleep(1) 
    # 히터 작동
    if float(temp) <= float(plant_dataset_temp): 
        gp.output(18,gp.HIGH)
    else:
        gp.output(18,gp.LOW)
    # 팬 작동
    if float(hd) >= float(plant_dataset_hd):
        gp.output(22,gp.HIGH)
    else:
        gp.output(22,gp.LOW)   
    
    # 토양 습도(물주기)
    if int(plant_dataset_moi) == 6: # 두 달에 한 번 관수 
        gp.output(23,gp.HIGH)
        time.sleep(20)
        gp.output(23,gp.LOW)
        time.sleep(86400)
    elif int(plant_dataset_moi) == 5: # 한 달에 한 번 관수
        gp.output(23,gp.HIGH)
        time.sleep(20)
        gp.output(23,gp.LOW)
        time.sleep(43200)
    elif int(plant_dataset_moi) == 4: # 화분 흙 대부분이 말랐을때 충분히 관수 
        if int(moi) <= 50:
            gp.output(23,gp.HIGH)
            time.sleep(20)
            gp.output(23,gp.LOW)
    elif int(plant_dataset_moi) == 3: # 토양 표면이 말랐을 때 충분히 관수 
        if int(moi) <= 300:
            gp.output(23,gp.HIGH)
            time.sleep(20)
            gp.output(23,gp.LOW)
    elif int(plant_dataset_moi) == 2: # 흙을 촉촉하게 유지함
        if int(moi) <= 700:
            gp.output(23,gp.HIGH)
            time.sleep(20)
            gp.output(23,gp.LOW)
    else: # elif int(plant_dataset_moi) == 1: # 항상 흙을 축축하게 유지함
        if int(moi) <= 900:
            gp.output(23,gp.HIGH)
            time.sleep(20)
            gp.output(23,gp.LOW)

if __name__ == "__main__":
    app.run(host="192.168.70.157", port=5022)