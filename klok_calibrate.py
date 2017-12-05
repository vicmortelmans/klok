import klok_lib
import calendar
import time


offset_file = open('offset.txt', 'r+', 0)
offset_file.seek(0)
offset_string = offset_file.read()
offset = int(offset_string)
new_offset_string = str(0)
offset_file.seek(0)
offset_file.truncate()
offset_file.write(new_offset_string)
offset_file.close()


calibration_file = open('calibration.txt', 'r+', 0)
calibration_file.seek(0)
calibration_string = calibration_file.read()
calibration = float(calibration_string)
new_calibration = calendar.timegm(time.gmtime()) / 60.0
new_calibration_string = str(new_calibration)
calibration_file.seek(0)
calibration_file.truncate()
calibration_file.write(new_calibration_string)
calibration_file.close()
minutes_since_calibration = new_calibration - calibration


correction_file = open('correction.txt', 'r+', 0)
correction_file.seek(0)
correction_string = correction_file.read()
correction = float(correction_string)
new_correction = correction * (minutes_since_calibration + offset) / minutes_since_calibration
new_correction_string = str(new_correction)
correction_file.seek(0)
correction_file.truncate()
correction_file.write(new_correction_string)
correction_file.close()

print >> klok_lib.log, "Calibration offset: %s -> %s; calibration: %s -> %s; correction: %s -> %s" % (offset_string, new_offset_string, calibration_string, new_calibration_string, correction_string, new_correction_string)

klok_lib.init()
klok_lib.turn(1, brake=2, step=klok_lib.bells_step)

