#!/bin/bash
exec 1> >(logger -s -t $(basename $0)) 2>&1
cd /home/pi/Public/klok
python klok3.py

