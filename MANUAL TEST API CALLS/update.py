import requests

url = 'http://127.0.0.1:8000/collection/1/'
headers = {'Authorization': 'Token d592f691e8d12a82e985c4e470442f077e5de6f8', 'content_type': 'application/json'}
payload = {
    'title': 'UPDATED collection11',
    'description': 'UPDATED Description of the collectio11n',
    'movies': [
        {
            'title': 'HEY11YY',
            'description': 'descrip11tion of the fsdg sfgv sfgv',
            'genres': 'SCIFI',
            'uuid': '213 '
        },
        {
            'title': 'HIII111II',
            'description': 'description of the sdf dsg fdgb ',
            'genres': 'FEELGOOD',
            'uuid': '222'
        },
    ]
}
resp = requests.put(url, headers=headers, json=payload)
print(resp.json())
