import klok_lib
import RPi.GPIO as GPIO
import time
import datetime
import os

klok_lib.init()


chime_done = False
bells_done = False
while True:
	klok_lib.calibrate()
	now = datetime.datetime.now()
	hour = now.hour % 12
	if now.minute < 59:
		minute = now.minute + 1  # setting the target for the new hands position
	else:
		hour = (hour + 1) % 12
		minute = 0
	hands = (60 * hour) + minute
	clock_hands_file = open("hands.txt", "r+", 0)
	clock_hands_file.seek(0)
	clock_hands_string = clock_hands_file.read()
	clock_hands_file.close()
	clock_hour = int(clock_hands_string[0:2]) % 12  # % 12 for in case someone enters 24H format in the file manually
	clock_minute = int(clock_hands_string[3:5])
	clock_hands = (60 * clock_hour) + clock_minute
	difference = abs(hands - clock_hands)  # difference in minutes
	direction = False if hands > clock_hands else True
	if difference > 6 * 60:
		difference = 12 * 60 - difference
		direction = not direction
	if difference > 0:
		print >> klok_lib.log, "hands = %s" % clock_hands
		print >> klok_lib.log, "time = %s" % hands
		print >> klok_lib.log, "target position is %d hours and %d minutes" % (hour, minute)
		print >> klok_lib.log, "hands.txt is '%s'" % clock_hands_string
		print >> klok_lib.log, "current position of the hands is %d hours and %d minutes" % (clock_hour, clock_minute)
		print >> klok_lib.log, "going to move the hands %d minutes" % difference
		count = difference * klok_lib.quarter_turns_per_minute * klok_lib.quarter_turns_per_minute_correction / float(4)
                print >> klok_lib.log, "quarter_turns_per_minute = %f" % klok_lib.quarter_turns_per_minute
                print >> klok_lib.log, "quarter_turns_per_minute_correction = %f" % klok_lib.quarter_turns_per_minute_correction
                print >> klok_lib.log, "count = %f" % count
		klok_lib.turn(count, dir=direction)
		steps = count * klok_lib.steps_per_turn
		klok_lib.cumul_float_minutes += difference if dir else -difference
		klok_lib.cumul_float_steps += steps
		klok_lib.cumul_actual_steps += int(steps)
		chime_done = False
		bells_done = False
		print >> klok_lib.log, "moved hands"
		clock_hands_string = "%02d:%02d" % (hour, minute)
		print >> klok_lib.log, "hands.txt is '%s'" % clock_hands_string
		print >> klok_lib.log, "cumul_float_minutes is %.4f" % klok_lib.cumul_float_minutes
		print >> klok_lib.log, "cumul_float_steps is %.4f" % klok_lib.cumul_float_steps
		print >> klok_lib.log, "cumul_actual_steps is %d" % klok_lib.cumul_actual_steps
		print >> klok_lib.log, "%.8f steps per minute" % (klok_lib.steps_per_turn * klok_lib.quarter_turns_per_minute * klok_lib.quarter_turns_per_minute_correction / 4.0)
		print >> klok_lib.log, "%.8f correction" % klok_lib.quarter_turns_per_minute_correction
		clock_hands_file = open("hands.txt", "r+", 0)
		clock_hands_file.seek(0)
		clock_hands_file.write(clock_hands_string)
		clock_hands_file.close()
	if minute in [1, 16, 31, 46] and not chime_done:
		chimes_count = (minute - 1) / 15 if minute > 1 else 4
		print >> klok_lib.log, "going to sound %d chimes" % chimes_count
		for i in range(0, chimes_count):
			klok_lib.turn(0.5, brake=8, step=klok_lib.chime_step)
		chime_done = True
	if minute == 1 and not bells_done:
		bells_count = hour if hour > 0 else 12
		print >> klok_lib.log, "going to sound the bells %d times" % bells_count
		time.sleep(1)
		for i in range (0, bells_count):
			klok_lib.turn(1, brake=2, step=klok_lib.bells_step)
		bells_done = True
	klok_lib.log.flush()
	os.fsync(klok_lib.log)
	time.sleep(1)

#GPIO.cleanup()

