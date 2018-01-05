from bottle import route, run, template, post, request
import calendar
import time
import klok_lib
 
# route for a GET request
@route('/adjust-clock')
def adjust_clock():
  direction = request.query.direction
  minutes = int(request.query.minutes)
  print "Adjusting clock %s minutes %s" % (minutes, direction)
  offset_file = open('offset.txt', 'r+', 0)
  offset_file.seek(0)
  offset_string = offset_file.read()
  offset = int(offset_string)
  if 'forward' in direction:
    offset += minutes
    dir = False
  else:
    offset -= minutes
    dir = True
  offset_string = str(offset)
  offset_file.seek(0)
  offset_file.truncate()
  offset_file.write(offset_string)
  offset_file.close()
  klok_lib.init()
  klok_lib.turn(minutes * klok_lib.quarter_turns_per_minute / float(4), brake=2, dir=dir)
  # return the HTML we want the user to see on screen
  return "<b>Adjustment done</b>"
 
# route for a GET request
@route('/calibrate-clock')
def calibrate_clock():
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

     
# run the server forever
run(host='0.0.0.0', port=35001)
