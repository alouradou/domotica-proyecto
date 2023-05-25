#!/usr/bin/env python
# -*- coding: utf8 -*-
# Version modifiee de la librairie https://github.com/mxgxw/MFRC522-python

import RPi.GPIO as GPIO
import hardware.rfid.MFRC522 as MFRC522
import signal
import time

# from main import GLOBALS
from mqtt.pub import MQTTPublish


class RFIDReader:
    def __init__(self):
        # self.nb_place = 10
        self.Led_verte = 35
        self.Led_rouge = 33
        self.servo_gpio = 12
        self.frequence = 35
        self.continue_reading = True
        self.GPIO_TRIGGER = 36
        self.GPIO_ECHO = 32

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.Led_verte, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Led_rouge, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.servo_gpio, GPIO.OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
        self.pwm = GPIO.PWM(self.servo_gpio, self.frequence)

        # signal.signal(signal.SIGINT, self.end_read)
        self.MIFAREReader = MFRC522.MFRC522()

        self.pwm.start(self.angle_to_percent(0))
        time.sleep(1)
        print("set a 0")

    def angle_to_percent(self, angle):
        if angle > 180 or angle < 0:
            return False

        start = 4
        end = 12.5
        ratio = (end - start) / 180
        angle_as_percent = angle * ratio
        return start + angle_as_percent

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

    def end_read(self, signal, frame):
        self.continue_reading = False
        self.pwm.stop()
        GPIO.cleanup()

    def read_rfid(self):
        print("Passer le tag RFID a lire")

        while self.continue_reading:
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

            if status == self.MIFAREReader.MI_OK:
                print("Carte detectee")

            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

            if status == self.MIFAREReader.MI_OK:
                uid = str(uid[0]) + "." + str(uid[1]) + "." + str(uid[2]) + "." + str(uid[3])
                print("UID de la carte : " + uid)
                MQTTPublish().publish("upm/mqtt/rfid/uid", uid)
                if ((uid[0] == 243) and (uid[1] == 5) and (uid[2] == 26) and (uid[3] == 154) and (GLOBALS.spots > 0)):
                    MQTTPublish().publish("upm/mqtt/rfid/open", True)
                    GPIO.output(self.Led_verte, GPIO.HIGH)
                    self.pwm.ChangeDutyCycle(self.angle_to_percent(90))
                    time.sleep(2)
                    print("LED verte allumee")
                    dist = self.distance()
                    print(dist)
                    while dist < 10.0:
                        print("voiture detectee")
                        time.sleep(0.5)
                        dist = self.distance()
                        print(dist)
                    GLOBALS.spots = GLOBALS.spots - 1

                    MQTTPublish().publish("upm/mqtt/spots", GLOBALS.spots)
                    time.sleep(1)
                    MQTTPublish().publish("upm/mqtt/rfid/open", False)
                    GPIO.output(self.Led_verte, GPIO.LOW)
                    self.pwm.ChangeDutyCycle(self.angle_to_percent(0))
                    time.sleep(1)
                    print("LED off moteur 0")
                else:
                    MQTTPublish().publish("upm/mqtt/rfid/open", False)
                    GPIO.output(self.Led_rouge, GPIO.HIGH)
                    print("LED rouge allumee")
                    time.sleep(2)
                    GPIO.output(self.Led_rouge, GPIO.LOW)

                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                self.MIFAREReader.MFRC522_SelectTag(uid)
                status = self.MIFAREReader.MFRC522_Auth(self.MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                if status == self.MIFAREReader.MI_OK:
                    self.MIFAREReader.MFRC522_Read(8)
                    self.MIFAREReader.MFRC522_StopCrypto1()
                else:
                    time.sleep(0.5)

                time.sleep(1)

# Exemple d'utilisation
# rfid_reader = RFIDReader()
# rfid_reader.read_rfid()
