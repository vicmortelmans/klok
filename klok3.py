#!/usr/bin/env python
import klok_lib
import klok_calibrate
import logging
import mido
import time
import datetime
import os
import RPi.GPIO as GPIO

def hands_from_hour_minute(hour, minute):
    hour = hour % 12  # [0..11 int]
    return (60 * hour) + minute  # [0..12*60-1 minutes int]

def hands_from_string(time):
    return hands_from_hour_minute(int(time[0:2]),int(time[3:5]))  # [0..12*60-1 minutes int]

def string_from_hour_minute(hour, minute):
    return "%02d:%02d" % (hour % 12, minute)

def read_hands_from_file():
    clock_hands_string = klok_lib.read_string_from_file('hands.txt')  # [HH:MM string]
    return clock_hands_string

# initialize the GPIO
klok_lib.init()

chime_done = False
bells_done = False
klok_silence_file = '/tmp/klok-silence'

# start approx 1 sec eternal loop
previous_on_spoke = False
now_on_spoke = False
hands_have_moved = False

while True:
    # this loop runs approx. every second
    # in this loop:
    # 1/ target [text] is the actual time ("HH:MM")
    # 2/ hands [{nr, text}] is the (best guess) of the current position of the hands ("HH:MM")
    #  - based on hands.txt (so you can correct hands by writing their actual position to hands.txt)
    #  - adjusted to nearest spoke, if detected

    # get actual time
    now = datetime.datetime.now()
    hour = now.hour % 12
    minute = now.minute
    target = string_from_hour_minute(hour, minute)  # HH:MM

    # get the estimated position of the hands
    hands = read_hands_from_file()

    # correct the estimation if the IR sensor sees a spoke
    if hands_have_moved:
        previous_on_spoke = now_on_spoke
        spoke_reading = klok_lib.read_spoke()
        now_on_spoke = spoke_reading
        logging.info("spoke reading: %s" % str(now_on_spoke))
        logging.info("assumed hands: %s" % hands)
        # calculate adjustment based on knowing we enter a spoke
        if not previous_on_spoke and now_on_spoke:
            # find the reference point nearest to the assumed hands position
            # this is where (most probably) the hands actually are
            adjustment = 15  # just largest, since we're looking for the minimum
            adjusted_hands = hands
            for ref_hour in range(12):
                for ref_minute in [11, 26, 41, 56]:
                    ref_hands = string_from_hour_minute(ref_hour, ref_minute)
                    ref_adjustment = klok_lib.path(hands_from_string(ref_hands), hands_from_string(hands), 12*60-1)
                    if abs(ref_adjustment) < abs(adjustment):
                        adjustment = ref_adjustment
                        adjusted_hands = ref_hands
            if abs(adjustment) > 5:
                logging.warning("passing spoke [11, 26, 41, 56] at assumed %s on target %s and adjustment %s: IGNORING probably ghost reading" % (hands, target, str(adjustment)))
            elif abs(adjustment) > 0:
                hands = adjusted_hands
                # add the adjustment to offset.txt
                offset = int(klok_lib.read_string_from_file('offset.txt'))
                offset += adjustment
                klok_lib.write_string_to_file('offset.txt', str(offset))
                logging.info("spoke confirmed hands; %s" % hands)
                if abs(offset) > 5:
                    correction = klok_calibrate.calibrate()
                    logging.info("passing spoke [11, 26, 41, 56] at assumed %s on target %s and adding %s minutes to offset: |%s| > 5, so recalibrating the speed to %s" % (hands, target, str(adjustment), str(offset), str(correction)))
                else:
                    logging.info("passing spoke [11, 26, 41, 56] at assumed %s on target %s and adding %s minutes to offset: %s" % (hands, target, str(adjustment), str(offset)))
            else:
                logging.info("passing spoke [12, 27, 42, 57] at assumed %s on target %s and no adjustment needed (%s)" % (hands, target, str(adjustment)))

    # read quarter_turns_per_minute_correction factor from file
    # note that this file is re-read in each loop, because it can
    # be changed outside of this process!
    klok_lib.read_correction()

    # calculate the shortest path to move the hands to actual time
    difference = klok_lib.path(hands_from_string(hands), hands_from_string(target), 12*60-1)  # [minutes int]
    direction = False if difference > 0 else True  # [boolean] when hands are behind, False, meaning to move forward
    difference = abs(difference)
    if difference > 0:
        logging.info("* * * " + str(now) + " * * *")
        logging.info("going to move the hands %d minutes %s" % (difference, "backward" if direction else "forward"))
        logging.info("new hands: %s" % target)
        # calculate number of turns with correction applied
        count = difference * klok_lib.quarter_turns_per_minute * klok_lib.quarter_turns_per_minute_correction / float(4)  # [turns float]
        logging.info("quarter_turns_per_minute = %f" % klok_lib.quarter_turns_per_minute)
        logging.info("quarter_turns_per_minute_correction = %f" % klok_lib.quarter_turns_per_minute_correction)
        logging.info("count = %f" % count)
        # drive the motor for the hands
        klok_lib.turn(count, dir=direction)
        logging.info("moved hands")
        # compose new assumed hands position string and write it to file
        klok_lib.write_string_to_file('hands.txt', target)
        # allow sounds
        chime_done = False
        bells_done = False
        hands_have_moved = True
    else:
        hands_have_moved = False
    if minute in [0, 15, 30, 45] and not chime_done and not os.path.isfile(klok_silence_file):
        chimes_count = minute // 15 if minute > 1 else 4
        logging.info("going to sound %d chimes" % chimes_count)
        for i in range(0, chimes_count):
            klok_lib.turn(0.5, motor="chimes")
            time.sleep(0.3)
        chime_done = True
    if minute == 0 and not bells_done and not os.path.isfile(klok_silence_file):
        bells_count = hour if hour > 0 else 12
        logging.info("going to sound the bells %d times" % bells_count)
        time.sleep(1)
        klok_lib.turn(bells_count/3, dir=True, motor="bells")
        bells_done = True
        mid = mido.MidiFile('hour1.mid')
        for msg in mid.play():
            if msg.type == 'note_on':
                klok_lib.play_solenoid(msg.note)
    # sleep
    time.sleep(1)

#GPIO.cleanup()

#import pdb;pdb.set_trace()
