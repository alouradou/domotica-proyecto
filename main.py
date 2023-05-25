import signal

from hardware.rfid.rfid_reader import RFIDReader as RFIDReader
import threading
import time
import mqtt.sub as mqtt_sub
import hardware.servo.servo as servo
import api.messages as api

global GLOBALS

GLOBALS = {
    "spots": 6,
    "welcomeMessage": "Bienvenido!",
    "outMessage": "Hasta luego!",
}

def mqtt_listen():
    mqtt_sub.MQTTClient(GLOBALS)


def servo_loop():
    servo.ServoControl() # not a loop



def main():
    rfid_reader = RFIDReader(GLOBALS)
    api_server = api.APIServer(GLOBALS,rfid_reader)

    mqtt_thread = threading.Thread(target=mqtt_listen)
    rfid_thread = threading.Thread(target=rfid_reader.read_rfid)
    api_thread = threading.Thread(target=api_server.run_server)
    # us_thread = threading.Thread(target=us_loop)

    mqtt_thread.start()
    rfid_thread.start()
    api_thread.start()
    # us_thread.start()

    # Attendre indéfiniment que les threads se terminent
    # (ne terminera jamais car ce sont des boucles infinies)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du programme...")
        # signal.signal(signal.SIGINT,rfid_reader.end_read)
        rfid_reader.end_read(None, None)
        rfid_thread.join()


if __name__ == "__main__":
    main()
