import klok_lib


offset_file = open('offset.txt', 'r+', 0)
offset_file.seek(0)
offset_string = offset_file.read()
offset = int(offset_string)
offset += 1
#offset -= 1
offset_string = str(offset)
offset_file.seek(0)
offset_file.truncate()
offset_file.write(offset_string)
offset_file.close()

klok_lib.init()

klok_lib.turn(klok_lib.quarter_turns_per_minute / float(4))
#klok_lib.turn(klok_lib.quarter_turns_per_minute / float(4), dir=True)
