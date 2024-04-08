from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class Player():
    _instance = None
    
    def __new__(cls, id, player, number, attempts, status):
        if not cls._instance():
            cls._instance = super().__new__(cls,id, player, number, attempts, status)
            cls._instance.player = player
            cls._instance.number = number
            cls._instance.attempts = []
            cls._instance.status = status
        return cls._instance
    
    def crear_partida(self, player, status):
        servidor = random.choice([1-100])
        attempts = self.calcular(player, servidor,)
        partida = {
            "id": len(self.attempts) + 1,
            "player": player,
            "number": 12,
            "attempts": attempts,
            "status": status,
        }
        self.attempts.append(partida)
        return partida
    
    def calcular(self, number, servidor):
        if number == servidor:
            return "Partida finalizada, Congratuations"
        elif number < servidor:
            return "El numero a adivinar es mayor"
        else:
            return "El numero a adivinar es menor"

    def obtener_partidas(self):
        return self.attempts
        
    
    def listar_partida(self):
        pass
    
class PlayerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/guess":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            game = Player()
            partida = game.crear_partida(data["elemento"])
            self.send_response(201)
            self.send_header("Content-type","application/json")
            self.end_headers()
            self.wfile.write(json.dumps(partida).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        game = Player(1,"Julian", 50, [], "En Progreso")
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
        server_address = ("",8000)
        httpd = HTTPServer(server_address, PlayerHandler)
        print("Iniciando servidor HTTP en puerto 8000")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()
if __name__ == "__main__":
    main()
    
