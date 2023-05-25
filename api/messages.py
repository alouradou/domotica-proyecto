import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import RPi.GPIO as GPIO


GLOBALS = {'welcomeMessage': ''}

# Classe de gestionnaire de requêtes
class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, rfid_reader, *args, **kwargs):
        self.rfid_reader = rfid_reader
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self): # cors policy (important for api calls)
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        data = json.loads(post_data.decode())
        message = data.get('message', '')

        # Modification de la variable GLOBALS['welcomeMessage']
        GLOBALS['welcomeMessage'] = message

        response_data = {'response': 'Hello, world!', 'input': message}

        if message == "exit":
            GPIO.output(11, GPIO.HIGH)
            self.rfid_reader.force_open()

            time.sleep(2)
            GPIO.output(13, GPIO.LOW)

        self.wfile.write(json.dumps(response_data).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, world! ' + self.path.encode())


class APIServer:
    def __init__(self, GLOBALS, rfid_reader):
        self.GLOBALS = GLOBALS
        self.rfid_reader = rfid_reader
        self.Led_verte = 13
        self.Led_rouge = 11

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.Led_verte, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Led_rouge, GPIO.OUT, initial=GPIO.LOW)



    # Point d'entrée principal
    def run_server(self):
        host = '192.168.137.8'
        port = 8000

        server = HTTPServer((host, port), lambda *args, **kwargs: RequestHandler(self.rfid_reader, *args, **kwargs))
        server.rfid_reader = self.rfid_reader
        server.Led_verte = self.Led_verte
        server.Led_rouge = self.Led_rouge
        print(f'Server running on {host}:{port}')

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

        server.server_close()
        print('Server stopped')
        GPIO.cleanup()

    def redefine_messages(self):
        print('Current welcome message:', GLOBALS['welcomeMessage'])
