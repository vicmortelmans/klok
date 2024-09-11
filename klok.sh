#!/bin/bash
exec 1> >(logger -s -t $(basename $0)) 2>&1
cd /home/vic/klok
source env/bin/activate
python klok3.py

