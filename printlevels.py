from lib.devices import MoistureSensor
from lib.utils import get_kpa
import time

sensor = MoistureSensor()

while True:

    moisture_ohms = sensor.get_moisture()

    moisture_kiloohms = moisture_ohms / 1000.0

    celsius = sensor.get_temperature()

    kpa = get_kpa(moisture_kiloohms, celsius)

    fahrenheit = (celsius * 9.0 / 5.0) + 32.0

    output = [
        'Reading %s' % 0,
        'Voltage %s' % 0,
        'Ohms %s' % moisture_ohms,
        'kOhms %s' % moisture_kiloohms,
        'kPa %s' % kpa,
        'Temp %s' % fahrenheit,
    ]

    print ' | '.join(output)

    time.sleep(1)
