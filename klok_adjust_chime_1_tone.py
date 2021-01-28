import klok_lib
import RPi.GPIO as GPIO

klok_lib.init()

# 1 tone
klok_lib.turn(0.1, brake=2, step=klok_lib.chime_step)

GPIO.output(klok_lib.sleep, False)

