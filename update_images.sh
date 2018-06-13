#!/bin/bash

green=`tput setaf 2`
red=`tput setaf 1`
reset=`tput sgr0`

echo '['$(awk '{print $1}' /proc/uptime)'] - ${green}UPDATING IMAGES${reset}'

rm -r /home/debian/Desktop/shared
mkdir /home/debian/Desktop/shared
mount.cifs //stnls02.lnls.br/CommonSystems_Sirius/BEAGLETemp/ /home/debian/Desktop/shared/ -o credentials=/home/debian/Desktop/Project_display/pwd.txt
    
echo '['$(awk '{print $1}' /proc/uptime)'] - Ending Script'>>/var/log/mount_shared.log

exit 0

