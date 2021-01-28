import klok_lib
import RPi.GPIO as GPIO

klok_lib.init()

try:
	while True:
                # half a sound
		klok_lib.turn(0.05, brake=2, step=klok_lib.chime_step)

except KeyboardInterrupt:
	GPIO.output(klok_lib.sleep, False)
	print 'Interrupted!'

