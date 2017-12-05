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

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(hands_step, GPIO.OUT)
	GPIO.setup(chime_step, GPIO.OUT)
	GPIO.setup(bells_step, GPIO.OUT)
	GPIO.setup(hands_dir, GPIO.OUT)
	GPIO.setup(sleep, GPIO.OUT)

init()

GPIO.output(sleep, True)

try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.output(sleep, False)
	print "Interrupted"
