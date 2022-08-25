from flask import Flask
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
        return """
        <html>
        <body>
        <script>
        function test(){
        fetch('http://192.168.30.114:5099/test?data=33')
        }
        test()
        </script>
        </body>
        </html>
    """
    
    return 'Hello'

if __name__ == '__main__':
    app.run('192.168.30.208', 8084)