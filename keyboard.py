#!/usr/bin/env python
import klok_lib
import asyncio
from sshkeyboard import listen_keyboard

# initialize the GPIO
klok_lib.init()

KEY2MIDI = {
        's': 60,
        'd': 64,
        'f': 69,
        'j': 71,
        'k': 84
        }

# Asynchronous function to simulate playing a note
async def play_note(key):
    print(key, end='', flush=True)
    klok_lib.play_solenoid(KEY2MIDI[key])

# This function will be triggered for key presses
async def handle_keypress(key):
    if key in ['s', 'd', 'f', 'j', 'k']:
        await play_note(key)
    elif key == 'esc':
        print("Exiting...")
        raise SystemExit

# Main function to listen for key presses
def main():
    print("Listening for key presses... Press 'esc' to exit.")
    listen_keyboard(on_press=handle_keypress, delay_second_char=0.02, delay_other_chars=0.02)

# Run the main function
if __name__ == "__main__":
    main()

