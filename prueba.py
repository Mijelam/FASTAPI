import requests

API_URL = 'http://127.0.0.1:8000/movies/'
params = {'category': 'Ciencia ficción'}

response = requests.get(API_URL, params=params)
print(response)

if response.status_code == 200:
    movies = response.json()
    print("Películas encontradas:", movies)
else:
    print("Error:", response.text)
