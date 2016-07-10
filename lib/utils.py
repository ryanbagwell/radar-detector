def get_volts(reading, input_volts=3.3):
    """ Convert a digital reading to volts """

    return (reading * input_volts) / 1024


def get_resistance(volts, amps):
    return volts / amps


def get_kpa(kohms, celsius):
    """ Conversion equations taken from
        http://www.kimberly.uidaho.edu/water/swm/calibration_watermark2.pdf

        Round to 6 decimal places for consistency

    """

    kohms = round(kohms, 6)
    celsius = round(celsius, 6)

    if kohms < 1:
        kpa = -20 * (kohms * (1 + 0.018 * (celsius - 24)) - 0.55)

    elif 1 < kohms < 8:
        kpa = round(-3.213 * kohms - 4.093, 6) / round(1 - 0.009733 * kohms - 0.01205 * celsius, 6)
    else:
        kpa = -2.246 - round(5.239 * kohms, 6) * (1 + 0.018 * (celsius - 24)) - round(0.06756**2, 6) * round(1 + 0.018 * (celsius - 24), 6)**2

    return round(kpa, 6)



