import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import RPi.GPIO as GPIO


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

        if message == "exit":
            print("Exit Activated")
            GPIO.output(self.Led_verte, GPIO.HIGH)
            self.pwm.ChangeDutyCycle(self.angle_to_percent(90))
            time.sleep(2)
            print("LED verte allumee out")
            dist = self.distance()
            print(dist)
            while dist < 10.0:
                print("voiture detectee")
                time.sleep(0.5)
                dist = self.distance()
                print(dist)
            self.GLOBALS['spots'] = self.GLOBALS['spots'] + 1


        self.wfile.write(json.dumps(response_data).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, world! ' + self.path.encode())

    def distance(self):
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        return distance

    def angle_to_percent(self, angle):
        if angle > 180 or angle < 0:
            return False

        start = 4
        end = 12.5
        ratio = (end - start) / 180
        angle_as_percent = angle * ratio
        return start + angle_as_percent



class APIServer:
    def __init__(self, GLOBALS):
        self.GLOBALS = GLOBALS
        self.Led_verte = 13
        self.Led_rouge = 11
        self.servo_gpio = 12
        self.frequence = 35

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        time.sleep(3)

        GPIO.setup(self.Led_verte, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Led_rouge, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.servo_gpio, GPIO.OUT)

        self.pwm = GPIO.PWM(self.servo_gpio, self.frequence)
        self.pwm.start(self.angle_to_percent(0))

        print("set a 0")



    # Point d'entrée principal
    def run_server(self):
        host = '192.168.137.8'
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
