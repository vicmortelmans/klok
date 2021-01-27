import klok_lib

klok_lib.init()

try:
	while True:
		klok_lib.turn(1, brake=4, step=klok_lib.bells_step)
except KeyboardInterrupt:
	GPIO.output(sleep, False)
	print 'Interrupted!'

