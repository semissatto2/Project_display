#!/bin/sh

#Script de configuração completa da BBB (Script burro, nao analisa erros.)
#Tornar este arquivo executável com $sudo chmod 777 faztudo.sh
#Banco de cores
green=`tput setaf 2`
red=`tput setaf 1`
reset=`tput sgr0`

#Avisos iniciais
echo "${red}AVISO: NÃO REINICIE OU DESERNEGIZE A BEAGLEBONE!${reset}"
echo "${red}AVISO: NÃO INTERROMPA (CTRL + C) ESTE SCRIPT DE CONFIGURAÇÃO!${reset}"
echo "${red}AVISO: A INTERRUPÇÃO DESTE SCRIPT PODE DANIFICAR O SISTEMA OPERACIONAL. EM CASO DE PROBLEMAS, FORMATE A BEAGLEBONE COM UM NOVO SISTEMA OPERACIONAL${reset}"
echo "${red}Script feito por ${green}mauricio.donatti@lnls.br${reset}"
sleep 2

sudo -i

apt-get update -y
apt-get upgrade -y
sudo apt-get -y dist-upgrade

apt-get install locales
dpkg-reconfigure locales


sudo dpkg-reconfigure tzdata

#Aviso na tela
#sudo chmod 777 /home/debian/Desktop/Project_display/OLD_scripts/updating_display.py
#sudo python /home/debian/Desktop/Project_display/OLD_scripts/updating_display.py &


echo "${green}Atualizando Debian e obtendo pacotes Python pip, Adafruit, Pygame, Xdotool, Unclutter, Samba...${reset}"
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus midori python-pygame -y
sudo pip install --upgrade pip
sudo pip install Adafruit_BBIO
sudo pip install paho-mqtt
sudo apt-get install xdotool -y
sudo apt-get install unclutter -y
sudo apt-get install cifs-utils -y
sudo apt-get -y autoremove
sudo apt-get clean

echo "${green}Debian atualizado. Todos pacotes foram obtidos com sucesso...${reset}"
sleep 5

echo 'debian ALL=(ALL:ALL) NOPASSWD:/home/debian/Desktop/Project_display/update_fw.sh' | sudo EDITOR='tee -a' visudo
echo 'debian ALL=(ALL:ALL) NOPASSWD:/home/debian/Desktop/Project_display/update_images.sh' | sudo EDITOR='tee -a' visudo


echo "${green}Clonando Repositório...${reset}"
cd /home/debian/Desktop/
sudo rm -r Project_display/
git clone https://github.com/semissatto2/Project_display.git
echo "${green}Repositório clonado com sucesso...${reset}"
sleep 5

echo "${green}Concedendo permissões às rotinas de automação...${reset}"
cd /home/debian/Desktop/Project_display/
chmod +x launcher_browser.sh
chmod +x update_images.sh
chmod +x update_fw.sh
echo "${green}Permissões concedidas...${reset}"
sleep 5

echo "${green}Copiando arquivos e configurando startup...${reset}"
cd /home/debian/Desktop/Project_display/
cp launcher.service /lib/systemd/launcher.service
rm /etc/systemd/system/launcher.service
ln -s /lib/systemd/launcher.service /etc/systemd/system/launcher.service
systemctl daemon-reload
systemctl enable /lib/systemd/launcher.service
echo "${green}Arquivos copiados...${reset}"
sleep 3

echo "${green}Beaglebone completamente configurada. Reiniciando...${reset}"
sudo reboot
