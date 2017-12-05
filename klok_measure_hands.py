import RPi.GPIO as GPIO
import time
import datetime

hands_step = 7
hands_dir = 12
chime_step = 15
bells_step = 13
sleep = 11
ms = 0.001
steps_per_turn = 513.0343
quarter_turns_per_minute = 0.4575751
brake = 2

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(hands_step, GPIO.OUT)
	GPIO.setup(chime_step, GPIO.OUT)
	GPIO.setup(bells_step, GPIO.OUT)
	GPIO.setup(hands_dir, GPIO.OUT)
	GPIO.setup(sleep, GPIO.OUT)

init()

GPIO.output(hands_step, False)
GPIO.output(sleep, True)
GPIO.output(hands_dir, False)
i = 0
try:
	while True:
		GPIO.output(hands_step, True)
		time.sleep(ms*brake)
		GPIO.output(hands_step, False)
		time.sleep(ms*brake)
		i += 1
		# print "%d" % i
except KeyboardInterrupt:
	GPIO.output(sleep, False)
	print "Interrupted at %d steps!" % i


