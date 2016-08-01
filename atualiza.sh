#! /usr/bin/env bash
export GOOGLE_API_KEY="no"
export GOOGLE_DEFAULT_CLIENT_ID="no"
export GOOGLE_DEFAULT_CLIENT_SECRET="no"

sudo mkdir /home/debian/Desktop/shared
sudo cp /home/debian/Desktop/shared/beamon.jpg /home/debian/Desktop/Project_display/beamon.jpg
sudo cp /home/debian/Desktop/shared/beamoff.jpg /home/debian/Desktop/Project_display/beamoff.jpg
sudo cp /home/debian/Desktop/shared/imminent.jpg /home/debian/Desktop/Project_display/imminent.jpg
sudo cp /home/debian/Desktop/shared/falha.jpg /home/debian/Desktop/Project_display/falha.jpg

sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' /home/debian/.config/chromium/Default/Preferences
chromium --kiosk --disable-infobars --disable-session-crashed-bubble http://10.2.105.115:8080/LinhaInfoWeb/
sudo sleep 25s
sudo xdotool search --class Chromium windowactivate
sudo xdotool key F5
unclutter -idle 1 -root
echo "press ctrl c to stop"
exit 0

#Este script deve ser colocado na pasta /usr/bin/
#OBS: deve ser baixado xdotool, unclutter!
#sudo apt-get install xdotool
#sudo apt-get install unclutter
