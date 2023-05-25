# from hardware.rfid.rfid_reader import RFIDReader
import threading
import time
import paho.mqtt.client as mqtt

def rfid_loop():
    while True:
        print("RFID loop: No card")
        time.sleep(5)

def mqtt_listen():
    print("MQTT listen")


def main():

    mqtt_thread = threading.Thread(target=mqtt_listen)
    rfid_thread = threading.Thread(target=rfid_loop)

    mqtt_thread.start()
    rfid_thread.start()

    # Attendre indéfiniment que les threads se terminent
    # (ne terminera jamais car ce sont des boucles infinies)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
