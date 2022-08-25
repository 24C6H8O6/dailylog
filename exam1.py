from flask import Flask, render_template
import RPi.GPIO as gp

gp.setmode(gp.BCM)
gp.setup(18,gp.OUT)

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/led')
def state():
    global led
    print(f'현재 led 상태 : {led}')
    return led

@app.route('/led/on')
def led_on():
    gp.output(18, gp.HIGH)
@app.route('/led/off')
def led_off():
    gp.output(18, gp.LOW)
if __name__ == '__main__':
    app.run(host='192.168.0.7', port=5022)