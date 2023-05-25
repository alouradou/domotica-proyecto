from hardware.rfid.rfid_reader import RFIDReader as RFIDReader
import threading
import time
import mqtt.sub as mqtt_sub
import hardware.presence.ultrasound as us
import hardware.servo.servo as servo


def rfid_loop():
    RFIDReader.RFIDReader()

def mqtt_listen():
    mqtt_sub.MQTTClient()

def us_loop():
    us.Ultrasound()

def servo_loop():
    servo.ServoControl() # not a loop


def main():

    mqtt_thread = threading.Thread(target=mqtt_listen)
    rfid_thread = threading.Thread(target=rfid_loop)
    us_thread = threading.Thread(target=us_loop)

    mqtt_thread.start()
    rfid_thread.start()
    us_thread.start()

    # Attendre indéfiniment que les threads se terminent
    # (ne terminera jamais car ce sont des boucles infinies)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
