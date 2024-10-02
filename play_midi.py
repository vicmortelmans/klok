#!/usr/bin/env python
import klok_lib
import asyncio
import mido

# initialize the GPIO
klok_lib.init()

mid = mido.MidiFile('flash1.mid')
for msg in mid.play():
    if msg.type == 'note_on':
        print(msg.note)
        klok_lib.play_solenoid(msg.note)

