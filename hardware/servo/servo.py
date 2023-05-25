import RPi.GPIO as GPIO
import time

global pwm_gpio, frequence, pwm

class ServoControl:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        pwm_gpio = 12
        frequence = 50
        GPIO.setup(pwm_gpio, GPIO.OUT)
        pwm = GPIO.PWM(pwm_gpio, frequence)

        # init at 0°
        pwm.start(self.angle_to_percent(0))
        time.sleep(1)
        print("0 degres")
        # Go at 90°
        pwm.ChangeDutyCycle(self.angle_to_percent(90))
        time.sleep(1)
        print(" moins 30 degres")
        # close GPIO & cleanup
        pwm.stop()
        GPIO.cleanup()

    def angle_to_percent(self,angle):
        if angle > 180 or angle < 0:
            return False

        start = 4
        end = 12.5
        ratio = (end - start) / 180
        angle_as_percent = angle * ratio
        return start + angle_as_percent