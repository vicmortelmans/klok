import RPi.GPIO as GPIO
import time
import datetime
import os

os.chdir('/home/pi/Public/klok')
hands_step = 7
hands_dir = 12
chime_step = 15
bells_step = 13
sleep = 11
ms = 0.001
steps_per_turn = 513.0343
quarter_turns_per_minute = 0.4381270354825263
quarter_turns_per_minute_correction = 1
running_behind = {}
running_behind[hands_step] = 0 
running_behind[chime_step] = 0 
running_behind[bells_step] = 0 
cumul_float_steps = 0
cumul_float_minutes = 0
cumul_actual_steps = 0

log = open('log.txt', 'a')

def calibrate():
	global quarter_turns_per_minute_correction
	correction_file = open('correction.txt', 'r+', 0)
	correction_file.seek(0)
	correction_string = correction_file.read()
	quarter_turns_per_minute_correction = float(correction_string)
	correction_file.close()


def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(hands_step, GPIO.OUT)
	GPIO.setup(chime_step, GPIO.OUT)
	GPIO.setup(bells_step, GPIO.OUT)
	GPIO.setup(hands_dir, GPIO.OUT)
	GPIO.setup(sleep, GPIO.OUT)


def turn(count, brake=4, dir=False, step=hands_step):  # at brake=1 steps are missed
	if count > 0:
		GPIO.output(step, False)
		GPIO.output(sleep, True)
		GPIO.output(hands_dir, dir)
		print >> log, "running behind %.4f steps before turn" % running_behind[step]
                steps = int(count * steps_per_turn)
                running_behind[step] += count * steps_per_turn - steps
		print >> log, "running behind %.4f steps without correction" % running_behind[step]
                if running_behind[step] > 1:
			steps += 1
			running_behind[step] -= 1
			print >> log, "running behind %.4f steps after correction" % running_behind[step]
		accelleration_brake = brake * 128
		start = time.time()
		for i in range(0, steps):
			GPIO.output(step, True)
			time.sleep(ms)
			GPIO.output(step, False)
			time.sleep(ms*accelleration_brake)
			if accelleration_brake > brake:
				accelleration_brake /= 2
			# print >> log, "%d" % i
		end = time.time()
		GPIO.output(sleep, False)
		elapsed = end - start
		print >> log, "%.4f turns, %d steps took %d seconds" % (count, steps, elapsed)
	else:
		print >> log, "no turns"


