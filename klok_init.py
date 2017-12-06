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

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(hands_step, GPIO.OUT)
	GPIO.setup(chime_step, GPIO.OUT)
	GPIO.setup(bells_step, GPIO.OUT)
	GPIO.setup(hands_dir, GPIO.OUT)
	GPIO.setup(sleep, GPIO.OUT)


def turn(count, brake=2, dir=False, step=hands_step):  # at brake=1 steps are missed
	if count > 0:
		GPIO.output(step, False)
		GPIO.output(sleep, True)
		GPIO.output(hands_dir, dir)
		start = time.time()
		for i in range(0,int(count * steps_per_turn)):
		  GPIO.output(step, True)
		  time.sleep(ms*brake)
		  GPIO.output(step, False)
		  time.sleep(ms*brake)
		  # print "%d" % i
		end = time.time()
		GPIO.output(sleep, False)
		elapsed = end - start
		print "%d turns took %d seconds" % (count, elapsed)
	else:
		print "no turns"


def up(id, s):
	# for testing, keep output <id> up for <s> s
	# if s = 0, keep up until interrupted
	GPIO.output(id, True)
	if s:
		time.sleep(s)
		GPIO.output(id, False)
	else:
		try:
			while True:
				pass
		except KeyboardInterrupt:
			GPIO.output(id, False)
			print 'Interrupted!'


init()

