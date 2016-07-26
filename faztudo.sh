#!/bin/sh
sudo ntpdate pool.ntp.org
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus -y
sudo pip install Adafruit_BBIO
sudo apt-get install python-pygame –y
cd /home/Debian/Desktop/
git clone https://github.com/semissatto2/Project_display.git
cd /home/Debian/Desktop/Project_display/
sudo chmod 777 GPIO_callback4_sem_browser.py
sudo chmod 777 GPIO_callback4.py
sudo chmod 777 myserv.sh
sudo cp myserv.sh /etc/init.d
sudo /etc/init.d/myserv.sh start
systemctl daemon-reload
sudo apt-get install xdotool -y
sudo apt-get install unclutter -y
cd /home/Debian/Desktop/Project_display/
sudo chmod 777 atualiza.sh
sudo cp atualiza.sh /usr/bin/
sudo mkdir /home/debian/.config/autostart/
cd /home/Debian/Desktop/Project_display/
sudo chmod 777 autoscript.desktop
sudo cp autoscript.desktop /home/debian/.config/autostart/autoscript.desktop

#Script de configuração completa da BBB 
#Tornar este arquivo executável com $sudo chmod 777 faztudo.sh
