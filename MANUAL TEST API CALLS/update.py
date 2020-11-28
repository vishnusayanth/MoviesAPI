import requests

url = 'http://127.0.0.1:8000/collection/2/'
headers = {'Authorization': 'Token d592f691e8d12a82e985c4e470442f077e5de6f8', 'content_type': 'application/json'}
payload = {
    'title': 'UPDATED collection11',
    'description': 'UPDATED Description of the collectio11n',
    'movies': [
        {'title': 'Queerama', 'description': '50 years after decriminalisation of homosexuality in the UK, director Daisy Asquith mines the jewels of the BFI archive to take us into the relationships, desires, fears and expressions of gay men and women in the 20th century.', 'genres': 'Mystery,Horror', 'uuid': '57baf4f4-c9ef-4197-9e4f-acf04eae5b4d'},
        {'title': 'Shadow of the Blair Witch', 'description': 'In this true-crime documentary, we delve into the murder spree that was the inspiration for Joe Berlingers "Book of Shadows: Blair Witch 2".', 'genres': 'Mystery,Horror', 'uuid': 'bcacfa33-a886-4ecb-a62a-6bbcb9d9509d'},
    ]
}
resp = requests.put(url, headers=headers, json=payload)
print(resp.json())
