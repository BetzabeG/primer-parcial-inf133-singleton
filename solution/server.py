from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class Player:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.attempts = []
        return cls._instance
    
    def crear_partida(self, player, number):
        servidor = random.randint(1, 100)
        status, message = self.calcular(number, servidor)
        partida = {
            "id": len(self.attempts) + 1,
            "player": player,
            "number": number,
            "server_number": servidor,
            "status": status,
            "message": message
        }
        self.attempts.append(partida)
        return partida
    
    def calcular(self, number, servidor):
        if number == servidor:
            return "Finalizada", "Felicidades"
        elif number < servidor:
            return "En Progreso", "El numero a adivinar es mayor"
        else:
            return "En Progreso", "El numero a adivinar es menor"

    def obtener_partidas(self):
        return self.attempts
        
class PlayerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/guess":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            player_name = data.get("player")
            number = data.get("number")
            game = Player()
            partida = game.crear_partida(player_name, number)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(partida).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        game = Player()
        if self.path == "/guess":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game.obtener_partidas()).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

        
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PlayerHandler)
        print("Iniciando servidor HTTP en puerto 8000")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()
