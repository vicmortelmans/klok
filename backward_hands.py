import klok_lib

offset = int(klok_lib.read_string_from_file('offset.txt'))
offset -= 1
klok_lib.write_string_to_file('offset.txt', str(offset))

klok_lib.init()

klok_lib.turn(klok_lib.quarter_turns_per_minute / float(4), dir=True)
