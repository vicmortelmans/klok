import klok_lib


offset_file = open('offset.txt', 'r+', 0)
offset_file.seek(0)
offset_string = offset_file.read()
offset = int(offset_string)
offset += 10
offset_string = str(offset)
offset_file.seek(0)
offset_file.truncate()
offset_file.write(offset_string)
offset_file.close()

klok_lib.init()

klok_lib.turn(10 *klok_lib.quarter_turns_per_minute / float(4))