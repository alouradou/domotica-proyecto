# Author: Alberto Brunete
#Modified by: Paloma de la Puente
# https://bitbucket.org/abrunete/practical_iot/wiki/Session%208%20-%20MQTT

import paho.mqtt.client as mqtt  #import the client1


broker_address="127.0.0.1" # Use the Raspberry Pi IP address
#broker_address="iot.eclipse.org"
#broker_address="broker.hivemq.com"
#broker_address="test.mosquitto.org"

client = mqtt.Client()

client.connect(broker_address, 1883, 60)

client.loop_start()    #start the loop

for n in range(1,5):
	client.publish("upm/mqtt",n) # Publicamos

client.disconnect()
client.loop_stop()

