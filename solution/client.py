
import requests
import json

url = "http://localhost:8000"
headers = {"Content-Type": "application/json"}

# Crear una partida nueva

response = requests.post(url=url +"/guess", json={"player": "Julian"}, headers=headers)
print(response.json())


# Listar todas las partidas

response = requests.get(url=url +"/guess")
print(response.json())

# Buscar una paartida por su id


