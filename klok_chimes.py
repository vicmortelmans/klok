import klok_lib
import RPi.GPIO as GPIO
import time

klok_lib.init()

while True:
    # 1/16th of a sound
    klok_lib.turn(0.313, motor="chimes")
    time.sleep(1.0)

GPIO.output(klok_lib.sleep, False)

