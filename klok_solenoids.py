import klok_lib
import RPi.GPIO as GPIO
import time

klok_lib.init()

try:
    while True:
        klok_lib.play_solenoid(60)
        time.sleep(0.5)
        klok_lib.play_solenoid(64)
        time.sleep(0.5)
        klok_lib.play_solenoid(69)
        time.sleep(0.5)
        klok_lib.play_solenoid(71)
        time.sleep(0.5)
        klok_lib.play_solenoid(84)
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.output(klok_lib.sleep, False)
    print('Interrupted!')
        

