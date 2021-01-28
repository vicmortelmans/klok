import klok_lib
import RPi.GPIO as GPIO

klok_lib.init()

# 1/16th of a sound
klok_lib.turn(0.00625, brake=2, step=klok_lib.chime_step)

GPIO.output(klok_lib.sleep, False)

