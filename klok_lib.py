import os
import time
import datetime
import logging
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

os.chdir('/home/vic/klok')

gpioPins = {}
gpioPins["bells"] = [0, 1, 5, 6]
gpioPins["hands"] = [15, 17, 18, 27]
gpioPins["chimes"] = [2, 3, 4, 14]
gpioPin_eye = 23
motor_driver = RpiMotorLib.BYJMotor("motor", "28BYJ")

# constants
ms = 0.001 # used to convert s to ms
steps_per_turn = 512.0  # [steps float]
quarter_turns_per_minute = 0.440710  # [turns float] default value, actual value if read from file

# corrections
quarter_turns_per_minute_correction = 1  # [factor float]
running_behind = {
    "hands": 0,  # [steps float] steps are discrete, so when advancing a non-integer number of steps,
    "chimes": 0,  # [steps float] the decimal part is stored here (for each motor), and when it
    "bells": 0   # [steps float] reaches 1, an extra step is performed
}

logging.basicConfig(format='[klok] %(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d %(funcName)s] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)


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
    GPIO.setmode(GPIO.BCM)
    for p in gpioPins["bells"] + gpioPins["hands"] + gpioPins["chimes"]: 
        GPIO.setup(p, GPIO.OUT)
    GPIO.setup(gpioPin_eye, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def turn(count, dir=False, motor="hands"):
    # count is a float saying how many turns the motor should make
    if count > 0:
        # calculate the steps
        steps = int(count * steps_per_turn)  # [steps int]
        # add one step if the accumulation of decimal steps reaches 1
        logging.info("running behind %.4f steps before turn" % running_behind[motor])
        running_behind[motor] += count * steps_per_turn - steps  # [steps float] decimal part of steps (not performed)
        if running_behind[motor] > 1:
            steps += 1  # [steps int]
            running_behind[motor] -= 1  # [steps float]
            logging.info("running behind %.4f steps after turn" % running_behind[motor])
        # initialize elapsed time
        start = time.time()
        # drive motor
        # motor_run(GPIOPins, wait, steps, counterclockwise, verbose, steptype, initdelay)
        motor_driver.motor_run(gpioPins[motor], 0.0010, steps, dir, False, "half", 0.001)
        # finish elapsed time
        end = time.time()
        # calculate elapsed time
        elapsed = end - start  # [s float]
        logging.info("%.4f turns, %d steps took %d seconds" % (count, steps, elapsed))
    else:
        logging.info("no turns")


def read_IR():
    return GPIO.input(gpioPin_eye) 

def read_spoke():
    IR  = GPIO.input(gpioPin_eye)  # reads 0 when on spoke 
    return not IR  # returns True when on spoke


def path(a, b, maximum):
    # calculate the shortest path from a to b in a cyclic range of number 0..maximum
    forward = b - a
    backward = b - a - maximum - 1 if b > a else b - a + maximum + 1
    if abs(forward) < abs(backward):
        return forward
    else:
        return backward
