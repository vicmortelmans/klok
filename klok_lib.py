import RPi.GPIO as GPIO
import time
import datetime
import os
import logging

os.chdir('/home/pi/Public/klok')

# GPIO pins
hands_step = 7  # step motor driving the hands
hands_dir = 12  # direction of motor driving the hands
chime_step = 15  # step motor driving the chime (tune each 15')
bells_step = 13  # step motor driving the bells (hour count)
sleep = 11  # enable/disable motors
IR_gpio = 16
chime_calibration_gpio = 17  # microswitch  # TODO

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
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(hands_step, GPIO.OUT)
    GPIO.setup(chime_step, GPIO.OUT)
    GPIO.setup(bells_step, GPIO.OUT)
    GPIO.setup(hands_dir, GPIO.OUT)
    GPIO.setup(sleep, GPIO.OUT)
    GPIO.setup(IR_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(chime_calibration_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # TODO


def turn(count, brake=4, calibration_gpio=None, calibration_point=None, dir=False, step=hands_step):  # brake 4 reaches longer than brake 2 or brake 8
    # count is a float saying how many turns the motor should make
    if count > 0:
        # initialize the motor for driving
        GPIO.output(step, False)
        GPIO.output(sleep, True)
        GPIO.output(hands_dir, dir)
        # calculate the steps
        steps = int(count * steps_per_turn)  # [steps int]
        # add one step if the accumulation of decimal steps reaches 1
        logging.info("running behind %.4f steps before turn" % running_behind[step])
        running_behind[step] += count * steps_per_turn - steps  # [steps float] decimal part of steps (not performed)
        if running_behind[step] > 1:
            steps += 1  # [steps int]
            running_behind[step] -= 1  # [steps float]
            logging.info("running behind %.4f steps after turn" % running_behind[step])
        # initialize accelleration
        accelleration_brake = brake * 256  # [ms int]
        # initialize elapsed time
        start = time.time()
        # drive motor
        i = 0
        i_final = steps
        calibrated = False
        while True:
            if not calibrated and  GPIO.input(calibration_gpio):
                # calibration_point is a [0..1] float indicating the point during this run where the switch should be hit
                i_calibration_point = calibration_point * i_final
                # e.g. i_final = 100; i_calibration_point = 50; i = 30
                #      then i_offset = -20
                i_offset = i - i_calibration_point 
                i_final += i_offset
                calibrated = True
            GPIO.output(step, True)
            time.sleep(pulse)
            GPIO.output(step, False)
            time.sleep(ms*accelleration_brake)
            if accelleration_brake > brake:
                accelleration_brake /= 2  # [ms int]
            if i >= i_final:
                break
            else:
                i += 1
                continue
        # finish elapsed time
        end = time.time()
        # put motor to sleep
        GPIO.output(sleep, False)
        # calculate elapsed time
        elapsed = end - start  # [s float]
        logging.info("%.4f turns, %d steps took %d seconds" % (count, steps, elapsed))
    else:
        logging.info("no turns")


def read_IR():
    return GPIO.input(IR_gpio) 

def read_spoke():
    # read IR_gpio ten times in a second; return:
    #  - None if result is not stable
    #  - True (1) or False (0) otherwise, whether or not on spoke
    for i in range(10):
        IR  = GPIO.input(IR_gpio)  # reads 0 when on spoke 
        if i > 0 and IR != previous_IR:
            logging.warning("Unstable eye reading")
            return None
        previous_IR = IR
    return not IR  # returns True when on spoke


def path(a, b, maximum):
    # calculate the shortest path from a to b in a cyclic range of number 0..maximum
    forward = b - a
    backward = b - a - maximum - 1 if b > a else b - a + maximum + 1
    if abs(forward) < abs(backward):
        return forward
    else:
        return backward
