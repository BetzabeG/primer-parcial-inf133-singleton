
import requests
import json

url = "http://localhost:8000"

# Crear una partida nueva
response = requests.post(url=url + "/guess", json={"player": "Julian"}, headers={"Content-Type": "application/json"})
print("Respuesta de crear partida:", response.json())

# Listar todas las partidas
response = requests.get(url=url + "/guess")
print(response.json())

# Buscar una partida por su id
game_id = 1  
response = requests.get(url=url + f"/guess/{game_id}")
print(response.json())


