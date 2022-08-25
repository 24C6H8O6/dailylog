import requests

def addWater(data1):
    data1 = 'Please add water'
    return requests.get(f"http://192.168.30.138:5011/test9?data={data1}")