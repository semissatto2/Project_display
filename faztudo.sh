#!/bin/sh
sudo ntpdate pool.ntp.org
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus -y
sudo pip install Adafruit_BBIO
sudo apt-get install python-pygame -y
cd /home/debian/Desktop/
git clone https://github.com/semissatto2/Project_display.git
cd /home/debian/Desktop/Project_display/
sudo chmod 777 GPIO_callback4_sem_browser.py
sudo chmod 777 GPIO_callback4.py
sudo chmod 777 display.sh
sudo chmod 777 launcher.service
sudo cp display.sh /usr/bin/display.sh
sudo cp launcher.service /lib/systemd/launcher.service
ln -s /lib/systemd/launcher.service /etc/systemd/system/launcher.service
sudo systemctl daemon-reload
sudo systemctl enable /lib/systemd/launcher.service
sudo apt-get install xdotool -y
sudo apt-get install unclutter -y
cd /home/debian/Desktop/Project_display/
sudo chmod 777 atualiza.sh
sudo cp atualiza.sh /usr/bin/atualiza.sh
sudo mkdir /home/debian/.config/autostart/
cd /home/debian/Desktop/Project_display/
sudo chmod 777 autoscript.desktop
sudo cp autoscript.desktop /home/debian/.config/autostart/autoscript.desktop
sudo systemctl start launcher.service





#Script de configuração completa da BBB 
#Tornar este arquivo executável com $sudo chmod 777 faztudo.sh
