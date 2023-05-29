# Domótica Proyecto

Este es el proyecto realizado para la clase de Domótica en la UPM, Madrid
presentado el 29 de mayo de 2023.

Here is the project realized for Domotics class in UPM, Madrid 
presented on 29th May, 2023.

## Setup

The project executes on a Raspberry Pi with a RFID reader, a LCD screen and a servo motor.

Distibution: Raspberry Pi OS.

## MQTT Broker

The setup the Pi's MQTT broker, follow the following instructions:
https://cedalo.com/blog/enabling-websockets-over-mqtt-with-mosquitto/

## Web Server

To **set up** the web server (On the Pi or on whatever computer):

```
cd web
npm install
```

To **run** the web server:

First, you need to change the local IP address of the Raspberry Pi in the files of the project:
- `./api/messages.py` line 70
- `./web/src/js/mqtt.js` line 5

Then, you can run the web server with:
```
cd web
npm run dev
```

You can access now access to the web server in the link given by Vite.js in the console.


Note that you can deploy the Front-End on the Raspberry with Apache installed, 
running `npm run build` and then putting the `dist` directory in the 
`/var/www/html` directory of the Raspberry Pi.


## Python Servers

Python thread including MQTT, Hardware, Web Server (API POST):

```
python main.py
```

Execute this command in the root folder of the project!

## Detailed hardware APIs

### LCD
To display on LCD:

```
import hardware.lcd.lcd_parking as lcd
lcd.LcdParking("string")
```

### Ultrasonic
To get distance from ultrasonic sensor:


More details in `hardware/rfid/rfif_reader.py`
in  `distance()` function:

```
import RPi.GPIO as GPIO

    GPIO.output(self.GPIO_TRIGGER, True)
    distance = (TimeElapsed * 34300) / 2
```

### Servo

All the interactions are in `hardware/rfid/rfif_reader.py`

## Fuentes:

- I2C LCD: https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/
- RFID: https://github.com/mxgxw/MFRC522-python
