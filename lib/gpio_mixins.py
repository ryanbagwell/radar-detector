import RPi.GPIO as GPIO
from numpy import median
import time


class ADCMixin(object):
    """ A class to read values from the
        mcp3008 analog-to-digital converter """

    def __init__(self, clk_pin=18, miso_pin=23, mosi_pin=24, cs_pin=25):

        self.clk_pin = clk_pin
        self.miso_pin = miso_pin
        self.mosi_pin = mosi_pin
        self.cs_pin = cs_pin

        self.setup()

    def setup(self):

        """ Set the pins for the mcp3008 """
        GPIO.setup(self.mosi_pin, GPIO.OUT)
        GPIO.setup(self.miso_pin, GPIO.IN)
        GPIO.setup(self.clk_pin, GPIO.OUT)
        GPIO.setup(self.cs_pin, GPIO.OUT)

    def read(self, channel_num=None):
        """ First, this method compiles and sends the
            sequence of bits to send to the mcp3008 in order
            to make it read the data from our analog sensors.

            Then, it 'bit bangs' the chip to read the data from
            items buffer
        """

        """ Throw an error if we haven't given a a channel number """
        if channel_num is None:
            raise ValueError('Please supply a channel number.')

        """ To initiate communication with the mcp3008,
            the cs pin has to be set to high, then back to low """
        GPIO.output(self.cs_pin, True)
        GPIO.output(self.cs_pin, False)

        """ We need to start with the click pin off, so turn it off
            in case it's on """
        GPIO.output(self.clk_pin, False)

        """ Compile the command that will tell the chip to
            read the analog values. It will consist of 5 bits
            composed of:

            1: a 0 start bit
            2: configuration mode (1 for single-ended, 0 for differential)
            3,4,5: channel number represented in binary notation:

                Channel 0: 000
                Channel 1: 001
                Channel 2: 010
                Channel 3: 011
                Channel 4: 100
                Channel 5: 101
                Channel 6: 100
                Channel 7: 111

        """

        """ Start with our channel number.

            Ex: in Binary, channel 4 will be represented
            as 0000 0100
        """
        commandout = channel_num

        """ The second bit signals the mcp3008 should use
            single-ended configuration mode. To do that, we use the
            bitwise 'OR' operator, which compares each bit and returns
            1 if 1 is in either operand, or 0 if 1 is not in either
            operand.

            To compute the desired result, we'll 'merge' the 0x18 bit
            (0001 1000) with the channel number bit, which will result
            in a byte whose last three bit contain the channel number,
            the fourth bit is a 1 (for the start bit) and the fifth bit
            is 1, which denotes single-ended mode.

            Ex: Channel 4: 0001 1100

        """
        commandout |= 0x18

        """ We only need the last four bits in our command. To do that, we use
            the left shift operator, which adds three zeros to the end of our
            command and only keeps the last 8 eight bits.

            Ex: channel 4: 1110 0000

        """

        commandout <<= 3

        """ Send the first five bits """
        for i in range(5):

            """ To decide if we need to set the output pin on (high) or off (low),
                we merge the 0x80 bit (1000 0000) with command string using the
                bitwise 'AND' operator, which results in 1 if both
                are in the operand, otherwise 0.

                This will provide results of either 0000 0000 or 1000 0000.

                In decimal, 0000 0000 is 0 (boolean False), and
                1000 000 is 128 (boolean True).

                After setting the pin, we'll shift the bits one
                place to the left and add a trailing zero. The next comparison
                will only look at the last 8 bits.

                The end effect is comparing the first 5 bits, and if they're 1,
                we'll set the pin to high. If they're 0, we'll set the pin to low.

                Ex: channel 4:

                1. 1110 0000 & 1000 0000   = 1000 0000 (128 or True)
                2. (1)110 0000 0 & 1000 0000 = 1000 0000 (128 or True)
                3. (11)10 0000 00 & 1000 0000 = 1000 000 (128 or True)
                4. (111)0 0000 000 = 1000 0000 = 0000 0000 (0 or False)
                5. (1110) 0000 0000 = 1000 0000 = 0000 0000 (0 or False)

                So essentially, we just sent: 1-1-1-0-0,
                or start-mode-channel-channel-channel

            """

            if (commandout & 0x80):
                GPIO.output(self.mosi_pin, True)
            else:
                GPIO.output(self.mosi_pin, False)

            """ Shift the command bits to the left """
            commandout <<= 1

            """ Turn the clock pin on and off to signal we're
                done sending the bit, and that the chip can expect
                the next bit """

            GPIO.output(self.clk_pin, True)
            GPIO.output(self.clk_pin, False)

        """ Now, read the data. Set a placeholder for
            the bits to receive. The first bit will be null,
            or 0. """
        adcout = 0

        """ The MCP3008 will give us 12 bits consiting of
            one empty bit, one null bit, and 10 data bits. """
        for i in range(12):

            """ Turn the clock pin on and off to forward the
                data buffer. """
            GPIO.output(self.clk_pin, True)
            GPIO.output(self.clk_pin, False)

            """ Shift the bit left by one place. """
            adcout <<= 1

            """ Read one bit from the chip's data output pin.
                The value will either be True or False.

                If the value is true, merge the value using the bitwise
                'OR' operator, which will always result in 1 for a
                value of True

            """

            if (GPIO.input(self.miso_pin)):
                adcout |= 0x1

        """ We're done reading the values. Set the CS pin to high
            to make it ready for our next read. """
        GPIO.output(self.cs_pin, True)

        """ The first bit is null, so remove it """
        adcout >>= 1

        """ Return our string of bits. """
        return adcout

    def sample(self, samples=30, channel_num=None):
        """ Returns the mean value of the number of readings
            taken. """

        readings = []

        for x in xrange(0, samples):

            value = self.read(channel_num=channel_num)
            readings.append(value)

        m = median(readings)

        return int(m)
