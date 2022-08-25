from flask import Flask,render_template,redirect,request
import requests
from multiprocessing import Process
import time
import sen_all
from concurrent.futures import ThreadPoolExecutor
import RPi.GPIO as gp
import pandas as pd

# ff.py에서 pyfirmata 불러오기
import sys
sys.path.append('/home/pi/pyFirmata')
import pyfirmata
board=pyfirmata.Arduino('/dev/ttyACM1')
pin13 = board.get_pin('d:13:o')

# gardenAll 데이터 불러오기
plant_data = pd.read_csv("gardenAll.csv", encoding="euc-kr")

app = Flask(__name__)

# 1. 히터(18),팬(22),물펌프(23) GPIO 값 설정
gp.setwarnings(False)
gp.setmode(gp.BCM)
gp.setup(18,gp.OUT)
gp.setup(22,gp.OUT)
gp.setup(23,gp.OUT)

# 2. temp(온도), hd(습도), lux(조도), waterA(급수), waterD(배수), moi(토양습도) 센서값 띄어쓰기로 분리
# 아두이노에서 받은 센서값 계속 오라클db로 전달
# 반복 작업
def get_url(url):
    return requests.get(url)
data = sen_all.data_send()
temp, hd, lux, waterA, waterD, moi = data.split(' ')
def sensor_data(data):
    for i in range(10):
        data = sen_all.data_send()
        temp, hd, lux, waterA, waterD, moi = data.split(' ')
pro1 = Process(args=(data,), target=sensor_data)
pro1.start()        
def tes(data):
    for i in range(10):
        list_of_urls = [f"http://192.168.70.151:8088?data={data}"]
        with ThreadPoolExecutor(max_workers=10) as pool:
            response_list = list(pool.map(get_url,list_of_urls))
        for response in response_list:
            print(response)
            time.sleep(10)
pro2 = Process(args=(data,), target=tes)
pro2.start()

# 급수 탱크(수위 조절)
# 반복 작업
def add_water(data):
    for i in range(3):
        if int(waterA) <= 120:
            water_add = 'Please add water'
            addWater = [f"http://192.168.70.151:8088/?data={water_add}"]
            with ThreadPoolExecutor(max_workers=10) as pool:
                response_list = list(pool.map(get_url,addWater))  
            for response in response_list:
                print(response)
                time.sleep(10)
pro3 = Process(args=(data,), target=add_water)
pro3.start()
# 배수 탱크(수위 조절)
# 반복 작업
def dump_water(data):
    for i in range(3):
        if int(waterD) >= 500:
            water_dump = 'Please dump water'
            dumpWater = [f"http://192.168.70.151:8088/?data={water_dump}"]
            with ThreadPoolExecutor(max_workers=10) as pool:
                response_list = list(pool.map(get_url,dumpWater))  
            for response in response_list:
                print(response)
                time.sleep(300)
pro4 = Process(args=(data,), target=dump_water)
pro4.start()

@app.route('/plant', methods=['GET'])
def plant():
    plant = request.args['plant']
    
@app.route('/web_data1', methods=['GET'])
def web_data1():
    plant = request.args['web_data1']
    
@app.route('/web_data2', methods=['GET'])
def web_data2():
    plant = request.args['web_data2']
    
@app.route('/web_data3', methods=['GET'])
def web_data3():
    plant = request.args['web_data3']
    
@app.route('/autocare', methods=['GET'])
def autocare():
    autocare = request.args['autocare']


plant = '청옥'
web_data1 = 'on'
web_data2 = 'on'
web_data3 = 'on'
autocare = 'on'



# 3-1. 수동 제어(html에서 각각의 토글스위치가 on/off되는 것에 <<function fan_on(){fetch('/fan/on')}>> 이런식으로 작성 필요)
# web_data : 웹에서 pc플라스크를 통해 들어오는 값
def auto_care(data):
    for i in range(10):
    # plant, web_data1, web_data2, web_data3, autocare ???
        if autocare == 'off':
            if web_data1 == 'on':
                web_data1 = gp.HIGH
            elif web_data1 == 'off':
                web_data1 = gp.LOW
            if web_data2 == 'on':
                web_data2 = gp.HIGH
            elif web_data2 == 'off':
                web_data2 = gp.LOW
            if web_data3 == 'on':
                web_data3 = gp.HIGH
            elif web_data3 == 'off':
                web_data3 = gp.LOW
            gp.output(18, web_data1)
            gp.output(22, web_data2)
            gp.output(23, web_data3)

    # 자동제어에서는 데이터베이스에서 plant_dataset_temp, plant_dataset_hd, plant_dataset_moi값을 요청해
    # 받아와서 제어
    # web에서 라프베리파이 플라스크로 보내주는 식물 이름을 plant 변수에 저장하여 각각의 데이터 뽑기

    # 3-2. 자동 제어
        if autocare == 'on':
            gp.output(18,gp.LOW)
            gp.output(22,gp.LOW)
            gp.output(23,gp.LOW)
            plant_data2 = plant_data[plant_data['name'] == plant]
    # web에서 라즈베리파이 플라스크로 보내주는 식물 이름을 plant 변수에 저장하여 각각의 데이터 뽑기
    # custom 데이터 보내줄 시 각각의 값을 변수에 저장하여 자동 제어
            plant_dataset_temp = plant_data2['temp(°C)']
            plant_dataset_hd = plant_data2['hd(%)']
            plant_dataset_moi = plant_data2['water']        
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
                if int(moi) <= 10:
                    gp.output(23,gp.HIGH)
                    time.sleep(5)
                    gp.output(23,gp.LOW)
                # time.sleep 설정 필요? 
            elif int(plant_dataset_moi) == 5: # 한 달에 한 번 관수
                if int(moi) <= 30:
                    gp.output(23,gp.HIGH)
                    time.sleep(5)
                    gp.output(23,gp.LOW)
                # time.sleep 설정 필요? 
            elif int(plant_dataset_moi) == 4: # 화분 흙 대부분이 말랐을때 충분히 관수 
                if int(moi) <= 50:
                    gp.output(23,gp.HIGH)
                    time.sleep(5)
                    gp.output(23,gp.LOW)
            elif int(plant_dataset_moi) == 3: # 토양 표면이 말랐을 때 충분히 관수 
                if int(moi) <= 300:
                    gp.output(23,gp.HIGH)
                    time.sleep(5)
                    gp.output(23,gp.LOW)
            elif int(plant_dataset_moi) == 2: # 흙을 촉촉하게 유지함
                if int(moi) <= 700:
                    gp.output(23,gp.HIGH)
                    time.sleep(5)
                    gp.output(23,gp.LOW)
            else: # elif int(plant_dataset_moi) == 1: # 항상 흙을 축축하게 유지함
                if int(moi) <= 900:
                    gp.output(23,gp.HIGH)
                    time.sleep(5)
                    gp.output(23,gp.LOW)
        print(i)
pro5 = Process(args=(data,), target=auto_care)
pro5.start()

neoPixel = 'on'
def led(data): 
    try:
        for i in range(10):
            if neoPixel = 'on':
                pin13.write(1)
                time.sleep(10)
                pin13.write(0)
                time.sleep(0)
            elif neoPixel = 'off':
                pin13.write(1)
                time.sleep(0)
                pin13.write(0)
                time.sleep(10)       
    except KeyboardInterrupt:
        gp.cleanup()
pro6 = Process(args=(data,), target=led)
pro6.start()

if __name__ == "__main__":
    app.run(host="192.168.70.9", port=5022)
pro1.join()
pro2.join()
pro3.join()
pro4.join()
pro5.join()
pro6.join()


