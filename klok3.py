#!/usr/bin/python
import klok_lib
import klok_calibrate
import logging
import RPi.GPIO as GPIO
import time
import datetime
import os

def hands_from_hour_minute(hour, minute):
	hour = hour % 12  # [0..11 int]
	return (60 * hour) + minute  # [0..12*60-1 minutes int]

def hands_from_string(time):
        return hands_from_hour_minute(int(time[0:2]),int(time[3:5]))  # [0..12*60-1 minutes int]

def string_from_hour_minute(hour, minute):
        return "%02d:%02d" % (hour % 12, minute)

# initialize the GPIO
klok_lib.init()

chime_done = False
bells_done = False
klok_silence_file = '/tmp/klok-silence'

# start approx 1 sec eternal loop
previous_on_spoke = None  
now_on_spoke = None
#import pdb;pdb.set_trace()
while True:
        # read quarter_turns_per_minute_correction factor from file
        # note that this file is re-read in each loop, because it can
        # be changed outside of this process!
	klok_lib.read_correction()
        # get actual time
	now = datetime.datetime.now()
        hour = now.hour % 12
        minute = now.minute
        hands = hands_from_hour_minute(hour, minute)  # [0..12*60-1 minutes int]
        hands_string = string_from_hour_minute(hour, minute)  # HH:MM
        # calculate the shortest path to move the hands to actual time
        clock_hands_string = klok_lib.read_string_from_file('hands.txt')  # [HH:MM string]
        clock_hands = hands_from_string(clock_hands_string)  # [0..12*60-1 minutes int]
        difference = klok_lib.path(clock_hands, hands, 12*60-1)  # [minutes int]
	direction = False if difference > 0 else True  # [boolean] when hands are behind, False, meaning to move forward
        difference = abs(difference)
	if difference > 0:
                logging.info("* * * " + str(now) + " * * *")
		logging.info("going to move the hands %d minutes %s" % (difference, "backward" if direction else "forward"))
		logging.info("new hands: %s" % hands_string)
                # calculate number of turns with correction applied
		count = difference * klok_lib.quarter_turns_per_minute * klok_lib.quarter_turns_per_minute_correction / float(4)  # [turns float]
                logging.info("quarter_turns_per_minute = %f" % klok_lib.quarter_turns_per_minute)
                logging.info("quarter_turns_per_minute_correction = %f" % klok_lib.quarter_turns_per_minute_correction)
                logging.info("count = %f" % count)
                # drive the motor for the hands
		klok_lib.turn(count, dir=direction)
		logging.info("moved hands")
                # compose new assumed hands position string and write it to file
                klok_lib.write_string_to_file('hands.txt', hands_string)
                # check if the IR sensor sees a spoke
                previous_on_spoke = now_on_spoke
                spoke_status = klok_lib.read_spoke()
                if spoke_status is not None:
                    now_on_spoke = spoke_status
                else:
                    logging.info("spoke status is undefined, keeping old reading")
                logging.info("spoke reading: %s" % str(now_on_spoke))
                # read assumed hands position from file
                # note that this file is re-read in each loop, because it can
                # be changed outside of this process!
                assumed_clock_hands_string = klok_lib.read_string_from_file('hands.txt')  # [HH:MM string]
                assumed_clock_hands = hands_from_string(assumed_clock_hands_string)  # [0..12*60-1 minutes int]
                clock_hands_string = assumed_clock_hands_string
                clock_hands = assumed_clock_hands
                logging.info("assumed hands: %s" % assumed_clock_hands_string)
                # calculate adjustment based on knowing we enter a spoke
                if previous_on_spoke is not None and now_on_spoke is not None and not previous_on_spoke and now_on_spoke:
                        logging.info("* * * " + str(now) + " * * *")
                        logging.info("passing spoke at assumed %s" % assumed_clock_hands_string)
                        # find the reference point nearest to the assumed hands position
                        # this is where (most probably) the hands actually are
                        adjustment = 15  # just largest, since we're looking for the minimum
                        for ref_hour in range(12):
                                for ref_minute in [12, 27, 42, 57]:
                                        ref_hands = hands_from_hour_minute(ref_hour, ref_minute)
                                        ref_adjustment = klok_lib.path(ref_hands, assumed_clock_hands, 12*60-1)
                                        if abs(ref_adjustment) < abs(adjustment):
                                                adjustment = ref_adjustment
                                                clock_hands = ref_hands
                                                clock_hands_string = string_from_hour_minute(ref_hour, ref_minute)
                        if adjustment:
                            # add the adjustment to offset.txt
                            offset = int(klok_lib.read_string_from_file('offset.txt'))
                            offset += adjustment
                            klok_lib.write_string_to_file('offset.txt', str(offset))
                            logging.info("spoke confirmed hands; %s" % clock_hands_string)
                            logging.info("passing spoke and adding %s minutes to offset" % str(adjustment))
                            if abs(offset) > 5:
                                    logging.info("offset |%s| > 5, so recalibrating the speed" % str(offset))
                                    klok_calibrate.calibrate()
                # allow sounds
		chime_done = False
		bells_done = False
	if minute in [0, 15, 30, 45] and not chime_done and not os.path.isfile(klok_silence_file):
		chimes_count = minute / 15 if minute > 1 else 4
		logging.info("going to sound %d chimes" % chimes_count)
		for i in range(0, chimes_count):
			klok_lib.turn(2.0, brake=3, step=klok_lib.chime_step)
		chime_done = True
	if minute == 0 and not bells_done and not os.path.isfile(klok_silence_file):
		bells_count = hour if hour > 0 else 12
		logging.info("going to sound the bells %d times" % bells_count)
		time.sleep(1)
                klok_lib.turn(bells_count, brake=2, step=klok_lib.bells_step)
                bells_done = True
        # sleep
	time.sleep(1)

#GPIO.cleanup()

