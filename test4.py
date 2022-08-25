import requests
import sen_all
data = sen_all.data_send()
def get_url(url):
    return requests.get(url)
for i in range(10):
    url = f"http://192.168.30.114:5099?data={data}"
    get_url(url)