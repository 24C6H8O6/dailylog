import requests
import time
import sen_all
from concurrent.futures import ThreadPoolExecutor

def get_url(url):
    return requests.get(url)
data = sen_all.data_send()
def tes(data):
    list_of_urls = [f"http://192.168.30.114:5099/test?data={data}"]

    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(get_url,list_of_urls))
        
    for response in response_list:
        print(response)

for i in range(10):
    tes(data)
    time.sleep(1)