#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

while :
do
	#Baixando versao do repositorio
	echo "Reading repository version ..."
	cd /home/debian/Downloads/
	wget -qN https://raw.githubusercontent.com/semissatto2/Project_display/master/version/version.txt # -N allows overwrite -q is quiet mode
	echo "Repository version successfully read"

	declare bbb_version=$(awk -F " " '/version/{print $3;}' /home/debian/Desktop/Project_display/version/version.txt)
	echo "BeagleboneBlack version is:" $bbb_version

	declare current_version=$(awk -F " " '/version/{print $3};' /home/debian/Downloads/version.txt)
	echo "Repository version is:" $current_version

	 if [ $bbb_version == $current_version ]; then
		echo "${green}Beaglebone is already UPDATED${reset}"
		sleep 60
	   else
		echo "${red}Beaglebone is OUTDATED${reset}"
		cd /home/debian/Downloads/
		sudo rm -r /home/debian/Downloads/Clones/
		echo "Cloning new Repository"
		sudo mkdir Clones
		cd /home/debian/Downloads/Clones/
		git clone https://github.com/semissatto2/Project_display.git
		sudo cp /home/debian/Downloads/Clones/Project_display/version/version.txt /home/debian/Desktop/Project_display/version/version.txt
		cd /home/debian/Downloads/Clones/Project_display/
		sudo chmod 777 faztudo.sh
		#sudo bash faztudo.sh
		echo "${green}Beaglebone now is UPDATED${reset}"
		sleep 60
		fi
done
