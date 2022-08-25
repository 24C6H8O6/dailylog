from flask import Flask, redirect
import sen_all
import time

app = Flask(__name__)


@app.route('/')
def index():
    result = sen_all.data_send()
    print(result)
    return redirect(f'http://192.168.30.114:8088/sensorUpload?data={result}')

if __name__ == '__main__':
    app.run('192.168.30.208', 8084)


