import paho.mqtt.client as mqtt

broker_address = "127.0.0.1"  # Use the Raspberry Pi IP address
# broker_address = "test.mosquitto.org"

class MQTTClient:
    def __init__(self, broker_address=broker_address, port=1883):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_address, port, 60)
        self.client.loop_forever()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")

        self.client.subscribe("upm/mqtt/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload.decode("utf-8")))

