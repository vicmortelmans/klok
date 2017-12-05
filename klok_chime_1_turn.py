import RPi.GPIO as GPIO
import time
step = 15
sleep = 11
ms = 0.001
steps_per_turn = 513.0343

def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(step, GPIO.OUT)
	GPIO.setup(sleep, GPIO.OUT)


def turn(count, brake=1):
	GPIO.output(step, False)
	GPIO.output(sleep, True)
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


init()
turn(1, brake=8)
GPIO.cleanup()

