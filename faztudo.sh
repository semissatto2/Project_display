#!/bin/sh
green=`tput setaf 2`
red=`tput setaf 1`

echo "${red}AVISO: NÃO REINICIE OU DESERNEGIZE A BEAGLEBONE"
echo "${red}AVISO: NÃO INTERROMPA (CTRL + C) ESTE SCRIPT DE CONFIGURAÇÃO"
echo "${red}AVISO: A INTERRUPÇÃO DESTE SCRIPT PODE DANIFICAR O SISTEMA OPERACIONAL. EM CASO DE PROBLEMAS, FORMATE A BEAGLEBONE COM UM NOVO SISTEMA OPERACIONAL"

echo "${green}Atualizando data do sistema..."
sudo ntpdate pool.ntp.org
echo "${green}Time stamp atualizado"
echo "${green}Atualizando data do sistema..."
echo "${green}Atualizando Debian e obtendo pacotes Python pip, Adafruit, Pygame, Xdotool, Unclutter, Samba..."
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus -y
sudo pip install Adafruit_BBIO
sudo apt-get install python-pygame -y
sudo apt-get install xdotool -y
sudo apt-get install unclutter -y
aptitude install cifs-utils -y
echo "${green}Debian atualizado. Todos pacotes foram obtidos com sucesso..."
sleep 5

echo "${green}Clonando Repositório..."
cd /home/debian/Desktop/
git clone https://github.com/semissatto2/Project_display.git
echo "${green}Repositório clonado com sucesso..."
sleep 5

echo "${green}Concedendo permissões 777 às rotinas de automação..."
cd /home/debian/Desktop/Project_display/
sudo chmod 777 GPIO_callback4_sem_browser.py
sudo chmod 777 GPIO_callback4.py
sudo chmod 777 display.sh
sudo chmod 777 launcher.service
sudo chmod 777 atualiza.service
sudo chmod 777 autoscript.desktop
sudo chmod 777 autoscript2.desktop
sudo chmod 777 atualiza.sh
sudo chmod 777 atualiza2.sh
echo "${green}Permissões concedidas..."
sleep 5

echo "${green}Copiando arquivos..."
cd /home/debian/Desktop/Project_display/
cp display.sh /usr/bin/display.sh
cp launcher.service /lib/systemd/launcher.service
cp atualiza.service /lib/systemd/atualiza.service
cp atualiza.sh /usr/bin/atualiza.sh
cp atualiza2.sh /usr/bin/atualiza2.sh
sudo mkdir /home/debian/.config/autostart/
cp autoscript.desktop /home/debian/.config/autostart/autoscript.desktop
cp autoscript2.desktop /home/debian/.config/autostart/autoscript2.desktop
echo "${green}Arquivos copiados..."
sleep 3

echo "${green}Incorporando scripts de automação ao sistema..."
ln -s /lib/systemd/launcher.service /etc/systemd/system/launcher.service
sudo systemctl daemon-reload
sudo systemctl enable /lib/systemd/launcher.service
ln -s /lib/systemd/atualiza.service /etc/systemd/system/atualiza.service
sudo systemctl daemon-reload
sudo systemctl enable /lib/systemd/atualiza.service
echo "${green}Scripts incorporados ao sistema..."
sleep 3



echo "${green}Inicializando os scripts de automação..."
sudo systemctl start launcher.service
sudo systemctl start atualiza.service
echo "${green}Beaglebone completamente configurada! Reiniciando"
sudo reboot



#Script de configuração completa da BBB 
#Tornar este arquivo executável com $sudo chmod 777 faztudo.sh
