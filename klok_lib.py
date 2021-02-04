import RPi.GPIO as GPIO
import time
import datetime
import os

os.chdir('/home/pi/Public/klok')

# GPIO pins
hands_step = 7  # step motor driving the hands
hands_dir = 12  # direction of motor driving the hands
chime_step = 15  # step motor driving the chime (tune each 15')
bells_step = 13  # step motor driving the bells (hour count)
sleep = 11  # enable/disable motors
IR_gpio = 16

# constants
ms = 0.001 # used to convert s to ms
pulse = 0.0005 # [s] step signal duration
steps_per_turn = 513.0343  # [steps float]
quarter_turns_per_minute = 0.4381270354825263  # [turns float] default value, actual value if read from file

# corrections
quarter_turns_per_minute_correction = 1  # [factor float]
running_behind = {
        hands_step: 0,  # [steps float] steps are discrete, so when advancing a non-integer number of steps,
        chime_step: 0,  # [steps float] the decimal part is stored here (for each motor), and when it
        bells_step: 0   # [steps float] reaches 1, an extra step is performed
}

log = open('log.txt', 'a')

def read_string_from_file(filename):
	file = open(filename, 'r+', 0)
	file.seek(0)
	string = file.read()
	file.close()
        return string


def write_string_to_file(filename, string):
        file = open(filename, "r+", 0)
        file.seek(0)
        file.truncate()
        file.write(string)
        file.close()


def read_correction():
        # read quarter_turns_per_minute_correction from file correction.txt
	global quarter_turns_per_minute_correction
	quarter_turns_per_minute_correction = float(read_string_from_file('correction.txt'))  # [factor float]


def init():
        # initialize GPIO
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(hands_step, GPIO.OUT)
	GPIO.setup(chime_step, GPIO.OUT)
	GPIO.setup(bells_step, GPIO.OUT)
	GPIO.setup(hands_dir, GPIO.OUT)
	GPIO.setup(sleep, GPIO.OUT)
        GPIO.setup(IR_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def turn(count, brake=4, dir=False, step=hands_step):  # brake 4 reaches longer than brake 2 or brake 8
        # count is a float saying how many turns the motor should make
	if count > 0:
                # initialize the motor for driving
		GPIO.output(step, False)
		GPIO.output(sleep, True)
		GPIO.output(hands_dir, dir)
                # calculate the steps
                steps = int(count * steps_per_turn)  # [steps int]
                # add one step if the accumulation of decimal steps reaches 1
		print >> log, "running behind %.4f steps before turn" % running_behind[step]
                running_behind[step] += count * steps_per_turn - steps  # [steps float] decimal part of steps (not performed)
                if running_behind[step] > 1:
			steps += 1  # [steps int]
			running_behind[step] -= 1  # [steps float]
			print >> log, "running behind %.4f steps after turn" % running_behind[step]
                # initialize accelleration
		accelleration_brake = brake * 256  # [ms int]
                # initialize elapsed time
		start = time.time()
                # drive motor
		for i in range(0, steps):
			GPIO.output(step, True)
			time.sleep(pulse)
			GPIO.output(step, False)
			time.sleep(ms*accelleration_brake)
			if accelleration_brake > brake:
				accelleration_brake /= 2  # [ms int]
			# print >> log, "%d" % i
                # finish elapsed time
		end = time.time()
                # put motor to sleep
		GPIO.output(sleep, False)
                # calculate elapsed time
		elapsed = end - start  # [s float]
		print >> log, "%.4f turns, %d steps took %d seconds" % (count, steps, elapsed)
	else:
		print >> log, "no turns"


def read_IR():
    return GPIO.input(IR_gpio) 


def path(a, b, maximum):
    # calculate the shortest path from a to b in a cyclic range of number 0..maximum
    forward = b - a
    backward = b - a - maximum - 1 if b > a else b - a + maximum + 1
    if abs(forward) < abs(backward):
        return forward
    else:
        return backward
