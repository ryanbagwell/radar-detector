from lib.devices import RadarDetector
import datetime
import os
import random
from time import sleep
import thread
import pytz
import logging

logging.addLevelName(25, 'VeggieBotInfo')

log_format = '%(levelname)s: %(asctime)s %(message)s'

logger = logging.getLogger('Veggiebot')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(log_format))

file_handler = logging.FileHandler('/var/log/veggiebot.log')
file_handler.setLevel(25)
file_handler.setFormatter(logging.Formatter(log_format))

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.log(25, "Starting monitor")



device = RadarDetector()

print device.read()












