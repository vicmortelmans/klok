import klok_lib
import calendar
import time
import logging

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
    offset_correction = offset / minutes_since_calibration
    offset_correction_cap = min(max(-0.1, offset_correction), 0.1)  # no corrections more than 10%
    new_correction = correction * (1 + offset_correction_cap)  # [float factor]

    klok_lib.write_string_to_file('correction.txt', str(new_correction))

    logging.info("Calibration offset: %s -> %s; calibration: %s -> %s; correction: %s -> %s (offset %s, min-since-last-cal %s)" % (str(offset), str(new_offset), str(calibration), str(new_calibration), str(correction), str(new_correction), str(offset), str(minutes_since_calibration)))
    if not offset_correction == offset_correction_cap:
        logging.warning("Change of correction capped at 10 percent, was originally %s percent" % (str(offset_correction * 100)))
    return new_correction

if __name__ == "__main__":
    klok_lib.init()
    calibrate()
    klok_lib.turn(1, brake=2, step=klok_lib.bells_step)
