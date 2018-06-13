#!/bin/bash

green=`tput setaf 2`
red=`tput setaf 1`
reset=`tput sgr0`

echo '['$(awk '{print $1}' /proc/uptime)'] - ${green}UPDATING FIRMWARE${reset}'

echo "${red}WARNING: THE BEAGLEBONE WILL AUTO REBOOT AFTER UPDATE${reset}"

echo "${green}Cloning repository${reset}"
cd /home/debian/Desktop/Project_display/
sudo git pull
echo "${green}Repository cloned succesfully...${reset}"

echo "${green}Giving permissions{reset}"
sudo chmod +x launcher_browser.sh
sudo chmod +x update_images.sh
sudo chmod +x update_fw.sh
echo "${green}Done...{reset}"

echo "${green}Configuring service at startup{reset}"
sudo cp launcher.service /lib/systemd/launcher.service
sudo rm /etc/systemd/system/launcher.service
sudo ln -s /lib/systemd/launcher.service /etc/systemd/system/launcher.service
sudo systemctl daemon-reload
sudo systemctl enable /lib/systemd/launcher.service
echo "${green}Done...{reset}"

echo "${green}Rebooting...{reset}"
sudo reboot