import signal

from hardware.rfid.rfid_reader import RFIDReader as RFIDReader
import threading
import time
import mqtt.sub as mqtt_sub
import hardware.servo.servo as servo

global GLOBALS

def mqtt_listen():
    mqtt_sub.MQTTClient(GLOBALS)


def servo_loop():
    servo.ServoControl() # not a loop


def main():
    GLOBALS = {
        "spots": 10,
        "welcomeMessage": "¡Bienvenido al parking!",
        "outMessage": "¡Hasta luego!",
    }
    rfid_reader = RFIDReader(GLOBALS)

    mqtt_thread = threading.Thread(target=mqtt_listen)
    rfid_thread = threading.Thread(target=rfid_reader.read_rfid)
    # us_thread = threading.Thread(target=us_loop)

    mqtt_thread.start()
    rfid_thread.start()
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
