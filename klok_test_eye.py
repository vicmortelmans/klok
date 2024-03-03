#!/usr/bin/python
import klok_lib
import time


# initialize the GPIO
klok_lib.init()

while True:
    current_IR = klok_lib.read_IR()  # 0 when on spoke (or when sensors not aligned)
    if current_IR:
        print("I can see you!")
    else:
        print("Nothing here...")
    time.sleep(0.1)
    #time.sleep(12.0)

