import requests,json

url = 'http://127.0.0.1:8000/collection'
headers = {'Authorization': 'Token d592f691e8d12a82e985c4e470442f077e5de6f8'}
resp = requests.get(url, headers=headers)
print(resp.json())