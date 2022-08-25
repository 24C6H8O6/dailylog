from flask import Flask, redirect, request
from multiprocessing import Process
import time

def cnt_number(start, end):
    for i in range(start, end + 1):
        print(i)
        time.sleep(0.5)
        
pro1 = Process(args=(1, 100), target=cnt_number)
pro1.start()

app = Flask(__name__)

num = '10'

@app.route('/', methods=['GET'])
def index():
    global num
    num = request.args['data']
    return num

@app.route('/out')
def output():
    global num
    return num

if __name__ == '__main__':
    app.run('192.168.70.113', 5021)

