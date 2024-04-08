import requests
import json

url = "http://localhost:8000"
# Crear una partida
print("\n***** crear una partida ****\n")
response = requests.post(url=url + "/guess", json={"player": "Julian"})
print(response.json())


# Listar todas las partidas
print("\n***** Listar todas las partidas ****\n")
response = requests.get(url=url + "/guess")
print(response.json())

#Actualizar los intentos de una partida
print("\n***** Actualizar los intentos de una partida ****\n")
response = requests.put(url=url + f"/guess/1", json={"attempt": 25})
print(response.json())

# Eliminar una partida.
print("\n***** eliminar una partida ****\n")
response = requests.delete(url=url + f"/guess/1")
print(response.json())

# Listar todas las partidas
print("\n***** Lista actual de las partidas ****\n")
response = requests.get(url=url + "/guess")
print(response.json())




