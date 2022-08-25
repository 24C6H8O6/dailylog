from flask import Flask,render_template,redirect,request
import requests
import sen_all
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

def get_url(url):
    return requests.get(url)
data = sen_all.data_send()
temp, hd, lux, waterA, waterD, moi = data.split(' ')
def tes(data):
    for i in range(10):
        list_of_urls = [f"http://192.168.70.104:5020/send?data={data}"]
        with ThreadPoolExecutor(max_workers=10) as pool:
            response_list = list(pool.map(get_url,list_of_urls)) 
        for response in response_list:
            print(response)

@app.route('/send', methods=['GET'])
def index():
    global num
    num = request.args['data']
    return num

'''@app.route('/', methods=['GET'])
def index():
    global num
    num = request.args['data']
    return num
    return redirect(f"http://192.168.70.104:5020/send")'''

tes(data)
if __name__ == "__main__":
    app.run(host="192.168.70.157", port=5022)