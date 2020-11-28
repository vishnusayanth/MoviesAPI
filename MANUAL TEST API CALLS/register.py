import requests

url = 'http://127.0.0.1:8000/register/'
payload = {
    'username': 'admin',
    'password': '123',
}
resp = requests.post(url,data=payload)
print(resp.json())
