#! /usr/bin/env bash
export GOOGLE_API_KEY="no"
export GOOGLE_DEFAULT_CLIENT_ID="no"
export GOOGLE_DEFAULT_CLIENT_SECRET="no"


sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' /home/debian/.config/chromium/Default/Preferences
chromium --kiosk --disable-infobars --disable-session-crashed-bubble http://10.2.105.115:8080/LinhaInfoWeb/
unclutter -idle 1 -root
echo "press ctrl c to stop"
exit 0

#Este script deve ser colocado na pasta /usr/bin/
#OBS: deve ser baixado xdotool, unclutter!
#sudo apt-get install xdotool
#sudo apt-get install unclutter
