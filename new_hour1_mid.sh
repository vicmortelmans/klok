#!/usr/bin/bash
cd /home/vic/klok
source env/bin/activate
./chatgpt_abc.py | ./abc_slow_tempo.py > hour.abc
abc2midi hour.abc
