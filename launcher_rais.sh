#!/usr/bin/env bash
export XAUTHORITY=~/.Xauthority
export DISPLAY=:0.0

unclutter &

python rais.py browser