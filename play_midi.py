#!/usr/bin/env python
import klok_lib
import asyncio
import mido
mid = mido.MidiFile('flash1.mid')
for msg in mid.play():
    if msg.type == 'note_on':
        klok_lib.play_solenoid(msg.note)

