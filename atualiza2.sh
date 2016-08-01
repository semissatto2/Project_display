#! /usr/bin/env bash
#Script de atualizacao do Chromium
for i in {0..10..2}
  do
    sleep 20s
    sudo xdotool search --class Chromium windowactivate
    sudo xdotool key F5
  done
exit 0
