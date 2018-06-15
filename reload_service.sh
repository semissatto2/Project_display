#!/bin/bash

pkill -9 -f rais.py
pkill midori
pkill chromium
pkill -9 -f launcher_rais.sh

export XAUTHORITY=~/.Xauthority
export DISPLAY=:0.0

python /home/debian/Desktop/Project_display/rais.py &
exit 0
