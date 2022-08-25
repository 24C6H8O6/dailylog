from flask import Flask
import sen_all
import time

app = Flask(__name__)

cnt = 0
@app.route('/')
def index():
    data = '5'
    while True:
        global cnt
        cnt += 1
        if cnt == 5:
            break
        time.sleep(1)
        temp = """
        <html>
        <body>
        <script>
        function test(){
        fetch('http://192.168.0.4:5011/test?data=6')
        }
        test()
        </script>
        </body>
        </html>
    """
        temp = temp.replace("!!!",data)
        return temp
    
    return 'Hello'

if __name__ == '__main__':
    app.run('192.168.0.7', 5022)