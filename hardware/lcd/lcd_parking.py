import hardware.lcd.I2C_LCD_driver as I2C_LCD_driver

from time import *


class LcdParking:
    def __init__(self,message):
        self.mylcd = I2C_LCD_driver.lcd()
        self.mylcd.lcd_display_string(str(message), 1)
