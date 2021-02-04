import klok_lib
import RPi.GPIO as GPIO

klok_lib.init()

try:
	while True:
		klok_lib.turn(1, brake=2, step=klok_lib.bells_step)

except KeyboardInterrupt:
	GPIO.output(klok_lib.sleep, False)
	print 'Interrupted!'
        

