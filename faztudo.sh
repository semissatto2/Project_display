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
sudo chmod 777 atualiza.service
cd /home/debian/Desktop/Project_display/
cp display.sh /usr/bin/display.sh
cd /home/debian/Desktop/Project_display/
cp launcher.service /lib/systemd/launcher.service
ln -s /lib/systemd/launcher.service /etc/systemd/system/launcher.service
sudo systemctl daemon-reload
sudo systemctl enable /lib/systemd/launcher.service
cd /home/debian/Desktop/Project_display/
cp atualiza.service /lib/systemd/atualiza.service
ln -s /lib/systemd/atualiza.service /etc/systemd/system/atualiza.service
sudo systemctl daemon-reload
sudo systemctl enable /lib/systemd/atualiza.service
sudo apt-get install xdotool -y
sudo apt-get install unclutter -y
cd /home/debian/Desktop/Project_display/
sudo chmod 777 atualiza.sh
cd /home/debian/Desktop/Project_display/
sudo chmod 777 atualiza2.sh
cd /home/debian/Desktop/Project_display/
cp atualiza.sh /usr/bin/atualiza.sh
cd /home/debian/Desktop/Project_display/
cp atualiza2.sh /usr/bin/atualiza2.sh
sudo mkdir /home/debian/.config/autostart/
cd /home/debian/Desktop/Project_display/
sudo chmod 777 autoscript.desktop
sudo chmod 777 autoscript2.desktop
cd /home/debian/Desktop/Project_display/
cp autoscript.desktop /home/debian/.config/autostart/autoscript.desktop
cd /home/debian/Desktop/Project_display/
cp autoscript2.desktop /home/debian/.config/autostart/autoscript2.desktop
sudo systemctl start launcher.service
sudo systemctl start atualiza.service




#Script de configuração completa da BBB 
#Tornar este arquivo executável com $sudo chmod 777 faztudo.sh
