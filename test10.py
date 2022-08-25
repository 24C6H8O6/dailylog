import requests
def get_url(url):
    return requests.get(url)
for i in range(10):
    url = f"http://192.168.30.138:5011?data={i}"
    get_url(url)
