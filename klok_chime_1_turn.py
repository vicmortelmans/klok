import klok_lib
import RPi.GPIO as GPIO

klok_lib.init()

# 5 tones (actually 4 + silence)
klok_lib.turn(2.0, brake=3, step=klok_lib.chime_step)

GPIO.output(klok_lib.sleep, False)

