#! /usr/bin/env bash
sudo echo '['$(awk '{print $1}' /proc/uptime)'] - Starting Script'>>/var/log/mount_shared.log

sudo rm -r /home/debian/Desktop/shared
sudo mkdir /home/debian/Desktop/shared
mount.cifs //stnls02.lnls.br/CommonSystems_Sirius/BEAGLETemp/ /home/debian/Desktop/shared/ -o credentials=/home/debian/Desktop/Project_display/pwd.txt
    
sudo echo '['$(awk '{print $1}' /proc/uptime)'] - Ending Script'>>/var/log/mount_shared.log

exit 0

