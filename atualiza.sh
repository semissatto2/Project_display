#! /usr/bin/env bash
export GOOGLE_API_KEY="no"
export GOOGLE_DEFAULT_CLIENT_ID="no"
export GOOGLE_DEFAULT_CLIENT_SECRET="no"
chromium --kiosk http://10.2.105.115:8080/LinhaInfoWeb/
sleep 25s
xdotool search --class Chromium windowactivate
xdotool key F5
unclutter -idle 1 -root
echo "press ctrl c to stop"
exit 0

#Este script deve ser colocado na pasta /usr/bin/
#OBS: deve ser baixado xdotool, unclutter!
