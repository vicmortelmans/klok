#!/usr/bin/python
import klok_lib

# initialize the GPIO
klok_lib.init()

# calculate turns for 1 minute
count = klok_lib.quarter_turns_per_minute * klok_lib.quarter_turns_per_minute_correction / float(4)  # [turns float]

# drive the motor for the hands
klok_lib.turn(count)
