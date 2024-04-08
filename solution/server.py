import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

class Partida:
    def __init__(self,player):
        self.id = None
        self.player = player
        self.number = random.randint(1, 100)
        self.attempts = []
        self.status = "En Progreso"

    def to_dict(self):
        return {"player": self.player,"number": self.number,"attempts": self.attempts,"status": self.status
        }

class Player:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.partidas = {}
            cls._instance.n_id = 1
        return cls._instance

    def crear_partida(self, player):
        partida = Partida(player)
        partida.id = self.n_id
        self.partidas[self.n_id] = partida
        self.n_id += 1
        return partida

    def listar_partidas(self):
        return {str(partida.id): partida.to_dict() for partida in self.partidas.values()}
    '''
    def buscar_partida_por_id(self,partida_id):
        return self.partidas.get(partida_id)
        '''

    def actualizar_intentos(self, partida_id, intento):
        partida = self.partidas.get(partida_id)
        if partida:
            partida.attempts.append(intento)
            if intento == partida.number:
                partida.status= "Finalizado"
                return "Felicitaciones"
            elif intento < partida.number:
                return "El numero a adivinar es mayor"
            else:
                return "El numero a adivinar es menor"
        else:
            return "Partida no encontrada"

    def eliminar_partida(self, partida_id):
        if partida_id in self.partidas:
            del self.partidas[partida_id]
            return "Partida eliminada"
        else:
            return "Partida no encontrada"

class RequestHandler(BaseHTTPRequestHandler):
    partida_manager = Player()

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        if self.path == '/guess':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            player = data.get('player')
            if player:
                partida = self.partida_manager.crear_partida(player)
                self._set_headers(201)
                self.wfile.write(json.dumps(partida.to_dict()).encode('utf-8'))
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "El nombre del jugador es requerido"}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Ruta no encontrada"}).encode('utf-8'))

    def do_GET(self):
        if self.path == '/guess':
            self._set_headers()
            self.wfile.write(json.dumps(self.partida_manager.listar_partidas()).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Ruta no encontrada"}).encode('utf-8'))

    def do_PUT(self):
        if self.path.startswith('/guess/'):
            partida_id = int(self.path.split('/')[-1])
            if partida_id:
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                data = json.loads(put_data.decode('utf-8'))
                intento = int(data.get('attempt'))
                mensaje = self.partida_manager.actualizar_intentos(partida_id, intento)
                self._set_headers()
                self.wfile.write(json.dumps({"message":mensaje}).encode('utf-8'))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error":"Partida no especificada"}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Ruta no encontrada"}).encode('utf-8'))

    def do_DELETE(self):
        if self.path.startswith('/guess/'):
            partida_id = int(self.path.split('/')[-1])
            if partida_id:
                mensaje =self.partida_manager.eliminar_partida(partida_id)
                self._set_headers()
                self.wfile.write(json.dumps({"message": mensaje}).encode('utf-8'))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Partida no especificada"}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Ruta no encontrada"}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('',port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nApagando servidor HTTP")
        httpd.server_close()

if __name__ == '__main__':
    run()
