from http.server import BaseHTTPRequestHandler, HTTPServer
import json

GLOBALS = {'welcomeMessage': ''}

# Classe de gestionnaire de requêtes
class RequestHandler(BaseHTTPRequestHandler):
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
        self.wfile.write(json.dumps(response_data).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, world! ' + self.path.encode())


class APIServer:
    def __init__(self, GLOBALS):
        self.GLOBALS = GLOBALS
        self.run_server()

    # Point d'entrée principal
    def run_server():
        host = 'localhost'
        port = 8000

        server = HTTPServer((host, port), RequestHandler)
        print(f'Server running on {host}:{port}')

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

        server.server_close()
        print('Server stopped')

    def redefine_messages(self):
        print('Current welcome message:', GLOBALS['welcomeMessage'])
