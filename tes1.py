from flask import Flask,render_template,redirect,request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    global num
    num = request.args['data']
    return redirect('http://192.168.70.104:5020/send') # num

if __name__ == "__main__":
    app.run(host="192.168.70.157", port=5022)