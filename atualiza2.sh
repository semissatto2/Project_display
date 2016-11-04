#! /usr/bin/env bash
#Script de atualizacao do Chromium
for i in {0..4..2}
  do
    sleep 20s
    sudo xdotool search --class Chromium windowactivate
    sudo xdotool key F5
    sudo mkdir /home/debian/Desktop/shared
    mount.cifs //centaurus/TROCA/gsemissatto/BBB /home/debian/Desktop/shared/ -o credentials=/home/debian/Desktop/Project_display/pwd.txt
    sudo cp /home/debian/Desktop/shared/* /home/debian/Desktop/Project_display/images/

  done
exit 0

#Deve ser colocado em /usr/bin/atualiza2.sh
