#!/bin/sh

#Banco de cores
green=`tput setaf 2`
red=`tput setaf 1`
reset=`tput sgr0`

#Avisos iniciais
echo "${red}AVISO: NÃO REINICIE OU DESERNEGIZE A BEAGLEBONE!${reset}"
echo "${red}AVISO: NÃO INTERROMPA (CTRL + C) ESTE SCRIPT DE CONFIGURAÇÃO!${reset}"
echo "${red}AVISO: A INTERRUPÇÃO DESTE SCRIPT PODE DANIFICAR O SISTEMA OPERACIONAL. EM CASO DE PROBLEMAS, FORMATE A BEAGLEBONE COM UM NOVO SISTEMA OPERACIONAL${reset}"
echo "${red}Script feito por ${green}guilherme.semissatto@lnls.br${reset}"
sleep 5

#Aviso na tela
sudo bash /home/debian/Desktop/Project_display/updating_display.py

echo "${green}Atualizando data do sistema...${reset}"
sudo ntpdate pool.ntp.org
echo "${green}Time stamp atualizado${reset}"
echo "${green}Atualizando Debian e obtendo pacotes Python pip, Adafruit, Pygame, Xdotool, Unclutter, Samba...${reset}"
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus -y
sudo pip install Adafruit_BBIO
sudo apt-get install python-pygame -y
sudo apt-get install xdotool -y
sudo apt-get install unclutter -y
aptitude install cifs-utils -y
echo "${green}Debian atualizado. Todos pacotes foram obtidos com sucesso...${reset}"
sleep 5

echo "${green}Clonando Repositório...${reset}"
cd /home/debian/Desktop/
git clone https://github.com/semissatto2/Project_display.git
echo "${green}Repositório clonado com sucesso...${reset}"
sleep 5

echo "${green}Concedendo permissões 777 às rotinas de automação...${reset}"
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
sudo chmod 777 compare.sh
echo "${green}Permissões concedidas...${reset}"
sleep 5

echo "${green}Copiando arquivos...${reset}"
cd /home/debian/Desktop/Project_display/
cp display.sh /usr/bin/display.sh
cp launcher.service /lib/systemd/launcher.service
cp atualiza.service /lib/systemd/atualiza.service
cp compare.service /lib/systemd/compare.service
cp compare.sh /usr/bin/compare.sh
cp atualiza.sh /usr/bin/atualiza.sh
cp atualiza2.sh /usr/bin/atualiza2.sh
sudo mkdir /home/debian/.config/autostart/
cp autoscript.desktop /home/debian/.config/autostart/autoscript.desktop
cp autoscript2.desktop /home/debian/.config/autostart/autoscript2.desktop
sudo mkdir /home/debian/Downloads/
cp /home/debian/Desktop/Project_display/version/version.txt /home/debian/Downloads/version.txt
echo "${green}Arquivos copiados...${reset}"
sleep 3

echo "${green}Incorporando scripts de automação ao sistema...${reset}"
ln -s /lib/systemd/launcher.service /etc/systemd/system/launcher.service
sudo systemctl daemon-reload
sudo systemctl enable /lib/systemd/launcher.service
ln -s /lib/systemd/atualiza.service /etc/systemd/system/atualiza.service
sudo systemctl daemon-reload
sudo systemctl enable /lib/systemd/atualiza.service
ln -s /lib/systemd/compare.service /etc/systemd/system/compare.service
sudo systemctl daemon-reload
sudo systemctl enable /lib/systemd/compare.service
echo "${green}Scripts incorporados ao sistema...${reset}"
sleep 3



echo "${green}Inicializando os scripts de automação...${reset}"
sudo systemctl start launcher.service
sudo systemctl start atualiza.service
sudo systemctl start compare.service
echo "${green}Beaglebone completamente configurada! Reiniciando...${reset}"
sudo reboot



#Script de configuração completa da BBB 
#Tornar este arquivo executável com $sudo chmod 777 faztudo.sh
