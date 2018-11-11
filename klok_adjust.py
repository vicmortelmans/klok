import klok_lib
import calendar
import time


offset_file = open('offset.txt', 'r+', 0)
new_offset_string = str(0)
offset_file.seek(0)
offset_file.truncate()
offset_file.write(new_offset_string)
offset_file.close()


calibration_file = open('calibration.txt', 'r+', 0)
new_calibration = calendar.timegm(time.gmtime()) / 60.0
new_calibration_string = str(new_calibration)
calibration_file.seek(0)
calibration_file.truncate()
calibration_file.write(new_calibration_string)
calibration_file.close()


print >> klok_lib.log, "Adjusting clock"

klok_lib.init()
klok_lib.turn(1, brake=2, step=klok_lib.bells_step)

