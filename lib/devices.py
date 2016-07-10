from .gpio_mixins import ADCMixin
import time
import datetime
import dateutil.parser
import RPi.GPIO as GPIO
import pytz


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Pin(object):
    """ A generic class to turn
        GOIP Pins on or off """

    def __init__(self, pin, mode=GPIO.BCM, warnings=False):
        self.pin = pin

    def status(self):
        """ Returns the status of the pin """

        return GPIO.input(self.pin)

    def on(self):
        """ Sets a pin to high """

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, True)

    def off(self):
        """ Sets a pin to low """

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)

    def toggle(self):

        if self.status() == 1:
            self.off()
        else:
            self.on()


class RadarDetector(ADCMixin):
    pass

