# Author: Alberto Brunete
#Modified by: Paloma de la Puente
# https://bitbucket.org/abrunete/practical_iot/wiki/Session%208%20-%20MQTT

import paho.mqtt.client as mqtt  #import the client1


broker_address="127.0.0.1" # Use the Raspberry Pi IP address
#broker_address="iot.eclipse.org"
#broker_address="broker.hivemq.com"
#broker_address="test.mosquitto.org"

class MQTTPublish:
    def __init__(self, broker_address=broker_address):
        self.broker_address = broker_address
        self.client = mqtt.Client()

    def publish(self, topic, message):
        self.client.connect(self.broker_address, 1883, 60)
        self.client.loop_start()
        self.client.publish(topic, message)
        self.client.disconnect()
        self.client.loop_stop()

