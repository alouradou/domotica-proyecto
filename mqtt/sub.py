import time

import paho.mqtt.client as mqtt
import hardware.lcd.lcd_parking as lcdparking
# from main import GLOBALS

broker_address = "127.0.0.1"  # Use the Raspberry Pi IP address
# broker_address = "test.mosquitto.org"

class MQTTClient:
    def __init__(self, GLOBALS, broker_address=broker_address, port=1883):
        self.GLOBALS = GLOBALS
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_address, port, 60)
        self.client.loop_forever()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        self.client.subscribe("upm/mqtt/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        # print in green
        print("\033[92m" + msg.topic + " " + str(msg.payload.decode("utf-8")) + "\033[0m")

        if msg.topic == "upm/mqtt/web":
            print("Broker connected to web")
        elif msg.topic == "upm/mqtt/presence":
            print("Presence state changed to " + str(msg.payload.decode("utf-8")))
        elif msg.topic == "upm/mqtt/spots":
            self.GLOBALS['spots'] = int(msg.payload.decode("utf-8"))
            lcdparking.LcdParking("Plazas: " + str(self.GLOBALS['spots']))
        elif msg.topic == "upm/mqtt/rfid/uid":
            print("RFID tag read: " + str(msg.payload.decode("utf-8")))
        elif msg.topic == "upm/mqtt/web/name1":
            print("Changing welcome message to " + str(msg.payload.decode("utf-8")))
            self.GLOBALS['welcomeMessage'] = str(msg.payload.decode("utf-8"))
        elif msg.topic == "upm/mqtt/web/name2":
            print("Changing out message to " + str(msg.payload.decode("utf-8")))
            self.GLOBALS['outMessage'] = str(msg.payload.decode("utf-8"))
        elif msg.topic == "upm/mqtt/rfid/open":
            print("RFID ok: " + str(msg.payload.decode("utf-8")))
            if str(msg.payload.decode("utf-8")) == "True":
                print("Opening door")
                lcdparking.LcdParking(self.GLOBALS['welcomeMessage'])
            if str(msg.payload.decode("utf-8")) == "False":
                print("Door staying closed")
                lcdparking.LcdParking(self.GLOBALS['outMessage'])













