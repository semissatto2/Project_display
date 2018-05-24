#! /usr/bin/env bash
export GOOGLE_API_KEY="no"
export GOOGLE_DEFAULT_CLIENT_ID="no"
export GOOGLE_DEFAULT_CLIENT_SECRET="no"

export XAUTHORITY=~/.Xauthority
export DISPLAY=:0.0

sudo echo $(awk '{print $1}' /proc/uptime)

sudo echo '['$(awk '{print $1}' /proc/uptime)'] - Starting Script'>>/home/debian/Desktop/Project_display/log.txt

while true
do
	ping -c 1 www.google.com.br
	if [[ $? == 0 ]];
	then
		sudo echo '['$(awk '{print $1}' /proc/uptime)'] - Network available.'>>/home/debian/Desktop/Project_display/log.txt
		break;
	else
		sudo echo '['$(awk '{print $1}' /proc/uptime)'] - Network is not available, waiting..'>>/home/debian/Desktop/Project_display/log.txt
		sleep 5
	fi
done

su debian -c "unclutter -idle 1 -root &"
su debian -c "midori -a https://status.lnls.br -e Fullscreen &"
#su debian -c "midori -a https://status.lnls.br"

echo "press ctrl c to stop"

sudo echo '['$(awk '{print $1}' /proc/uptime)'] - Starting Loop'>>/home/debian/Desktop/Project_display/log.txt

exit 0

for i in {0..4..2}
  do
    sleep 20s
    sudo mkdir /home/debian/Desktop/shared
    mount.cifs //stnls02.lnls.br/CommonSystems_Sirius/BEAGLETemp/ /home/debian/Desktop/shared/ -o credentials=/home/debian/Desktop/Project_display/pwd.txt
    #sudo cp /home/debian/Desktop/shared/* /home/debian/Desktop/Project_display/images/

  done

sudo echo '['$(awk '{print $1}' /proc/uptime)'] - Ending Script'>>/home/debian/Desktop/Project_display/log.txt

exit 0

#Este script deve ser colocado na pasta /usr/bin/
#OBS: deve ser baixado xdotool, unclutter!
#sudo apt-get install xdotool
#sudo apt-get install unclutter
