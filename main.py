from hardware.rfid.rfid_reader import RFIDReader


def main():
    import threading
    import time
    import paho.mqtt.client as mqtt

    # Importez votre classe RFIDReader ici
    # from rfid_reader import RFIDReader

    # Créez une instance de la classe RFIDReader
    rfid_reader = RFIDReader()

    # Fonction de rappel pour la réception des messages MQTT
    def on_message(client, userdata, message):
        # Traitez le message MQTT ici
        print("Message reçu :", message.payload.decode())

    # Fonction pour lancer l'écoute MQTT dans un thread
    def mqtt_listen():
        # Créez un client MQTT
        client = mqtt.Client()

        # Définissez les fonctions de rappel pour la connexion et la réception des messages
        client.on_connect = lambda client, userdata, flags, rc: print("Connecté au broker MQTT")
        client.on_message = on_message

        # Connectez-vous au broker MQTT
        client.connect("localhost", 1883, 60)

        # Abonnez-vous à un ou plusieurs sujets MQTT
        client.subscribe("topic1")
        client.subscribe("topic2")

        # Boucle principale MQTT (sera exécutée dans un thread séparé)
        client.loop_forever()

    # Fonction pour exécuter la boucle read_rfid dans un thread
    def rfid_loop():
        rfid_reader.read_rfid()

    # Lancez les deux fonctions dans des threads séparés
    mqtt_thread = threading.Thread(target=mqtt_listen)
    rfid_thread = threading.Thread(target=rfid_loop)

    mqtt_thread.start()
    rfid_thread.start()

    # Attendez indéfiniment que les threads se terminent (ne terminera jamais car ce sont des boucles infinies)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
