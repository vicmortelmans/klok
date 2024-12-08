import klok_lib
import RPi.GPIO as GPIO

klok_lib.init()

try:
    klok_lib.turn(1/3, dir=True, motor="bells")

except KeyboardInterrupt:
    GPIO.output(klok_lib.sleep, False)
    print('Interrupted!')
        

