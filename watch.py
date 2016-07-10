from lib.garden import Garden
import os
import random

garden = Garden()

moisture = garden.sample_mcp3008(channel_num=0)

print "Moisture level: %s" % moisture


def speak(message):

    gender = random.choice(['m','f',])
    variant = random.choice(range(1,7))

    voice = "-ven-us+%s%s" % (gender, variant)

    cmd = "espeak '%s' -s 160 %s" % (message, voice)
    print cmd
    os.system(cmd)


if moisture < garden.moisture_threshold:
    print "Stopping pump ..."
    result = os.system('insteonic irrigation off')
    print "Result: %s" % result
    speak("The garden is good!")
    #garden.notify("Stopped watering the garden. Moisture level: %s." % moisture)

elif moisture > 950:
    speak("You need to water the garden")
    #garden.notify("Started watering the garden. Moisture level: %s." % moisture)
    print os.system('insteonic irrigation on')
