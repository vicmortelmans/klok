#!/usr/bin/python
import klok_lib
import RPi.GPIO as GPIO
import time
import datetime
import os

# initialize the GPIO
klok_lib.init()

chime_done = False
bells_done = False
klok_silence_file = '/tmp/klok-silence'

# start approx 1 sec eternal loop
while True:
        # read quarter_turns_per_minute_correction factor from file
        # note that this file is re-read in each loop, because it can
        # be changed outside of this process!
	klok_lib.calibrate()
        # get actual time
	now = datetime.datetime.now()
	hour = now.hour % 12  # [0..11 int]
        # add one minute
	if now.minute == 59:
		hour = (hour + 1) % 12  # [0..11 int]
		minute = 0  # [0..59 int]
	else:
		minute = now.minute + 1  # [0..59 int]
	hands = (60 * hour) + minute  # [0..12*60-1 minutes int]
        # read assumed hands position from file
        # note that this file is re-read in each loop, because it can
        # be changed outside of this process!
        clock_hands_string = read_string_from_file('hands.txt')  # [HH:MM string]
	clock_hour = int(clock_hands_string[0:2]) % 12  # [0..11 int] % 12 for in case someone enters 24H format in the file manually
	clock_minute = int(clock_hands_string[3:5])  # [0..59 int]
	clock_hands = (60 * clock_hour) + clock_minute  # [0..12*60-1 minutes int]
	difference = abs(hands - clock_hands)  # [minutes int] 
	direction = False if hands > clock_hands else True  # [boolean] when hands are behind, False, meaning to move forward
	if difference > 6 * 60:
                # take the shorter route
		difference = 12 * 60 - difference  # [minutes int]
		direction = not direction
	if difference > 0:
		print >> klok_lib.log, "hands = %s" % clock_hands
		print >> klok_lib.log, "time = %s" % hands
		print >> klok_lib.log, "target position is %d hours and %d minutes" % (hour, minute)
		print >> klok_lib.log, "hands.txt is '%s'" % clock_hands_string
		print >> klok_lib.log, "current position of the hands is %d hours and %d minutes" % (clock_hour, clock_minute)
		print >> klok_lib.log, "going to move the hands %d minutes" % difference
                # calculate number of turns with correction applied
		count = difference * klok_lib.quarter_turns_per_minute * klok_lib.quarter_turns_per_minute_correction / float(4)  # [turns float]
                print >> klok_lib.log, "quarter_turns_per_minute = %f" % klok_lib.quarter_turns_per_minute
                print >> klok_lib.log, "quarter_turns_per_minute_correction = %f" % klok_lib.quarter_turns_per_minute_correction
                print >> klok_lib.log, "count = %f" % count
                # drive the motor for the hands
		klok_lib.turn(count, dir=direction)
		print >> klok_lib.log, "moved hands"
                # compose new assumed hands position string and write it to file
		clock_hands_string = "%02d:%02d" % (hour, minute)
                klok_lib.write_string_to_file('hands.txt', clock_hands_string)
		print >> klok_lib.log, "hands.txt is '%s'" % clock_hands_string
                # allow sounds
		chime_done = False
		bells_done = False
	if minute in [1, 16, 31, 46] and not chime_done and not os.path.isfile(klok_silence_file):
		chimes_count = (minute - 1) / 15 if minute > 1 else 4
		print >> klok_lib.log, "going to sound %d chimes" % chimes_count
		for i in range(0, chimes_count):
			klok_lib.turn(0.5, brake=2, step=klok_lib.chime_step)
		chime_done = True
	if minute == 1 and not bells_done and not os.path.isfile(klok_silence_file):
		bells_count = hour if hour > 0 else 12
		print >> klok_lib.log, "going to sound the bells %d times" % bells_count
		time.sleep(1)
                klok_lib.turn(bells_count, brake=1, step=klok_lib.bells_step)
                bells_done = True
	klok_lib.log.flush()
	os.fsync(klok_lib.log)
	time.sleep(1)

#GPIO.cleanup()

