import klok_lib
import calendar
import time

def calibrate():
    # read and reset offset
    offset = int(klok_lib.read_string_from_file('offset.txt'))  # [int min]
    new_offset = 0
    klok_lib.write_string_to_file('offset.txt', str(new_offset))

    # read time of last calibration, reset it and calculate minutes passed
    calibration = float(klok_lib.read_string_from_file('calibration.txt'))  # [int min last calibration since epoch]
    new_calibration = calendar.timegm(time.gmtime()) / 60.0  # [int min now since epoch]
    klok_lib.write_string_to_file('calibration.txt', str(new_calibration))
    minutes_since_calibration = new_calibration - calibration  # [int min]

    # read quarter_turns_per_minute_correction from file, calculate new correction and store it
    correction = float(klok_lib.read_string_from_file('correction.txt'))  # [float factor]
    new_correction = correction * (minutes_since_calibration + offset) / minutes_since_calibration  # [float factor]
    klok_lib.write_string_to_file('correction.txt', str(new_correction))

    print >> klok_lib.log, "Calibration offset: %s -> %s; calibration: %s -> %s; correction: %s -> %s" % (str(offset), str(new_offset), str(calibration), str(new_calibration), str(correction), str(new_correction))


klok_lib.init()
calibrate()
klok_lib.turn(1, brake=2, step=klok_lib.bells_step)

