import klok_lib
import RPi.GPIO as GPIO

klok_lib.init()

# 5 tones (actually 4 + silence)
klok_lib.turn(0.5, motor="chimes")

