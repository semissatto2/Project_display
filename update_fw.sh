#!/bin/bash

echo 'UPDATING FIRMWARE'
echo "WARNING: THE BEAGLEBONE WILL AUTO REBOOT AFTER UPDATE"

echo "Cloning repository"
cd /home/debian/Desktop/
sudo rm -r Project_display/
git clone https://github.com/semissatto2/Project_display.git
echo "Repository cloned succesfully..."

cd /home/debian/Desktop/Project_display
echo "Giving permissions"
chmod +x launcher_browser.sh
chmod +x launcher_rais.sh
chmod +x stop_service.sh
chmod +x update_images.sh
chmod +x update_fw.sh
echo "Done..."

echo "Configuring service at startup"
cp launcher.service /lib/systemd/launcher.service
rm /etc/systemd/system/launcher.service
ln -s /lib/systemd/launcher.service /etc/systemd/system/launcher.service
systemctl daemon-reload
systemctl enable /lib/systemd/launcher.service
echo "Done..."

#echo "Rebooting..."
#reboot

echo "Restarting service..."
systemctl reload launcher.service

exit 0
