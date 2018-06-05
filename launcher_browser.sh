#!/usr/bin/env bash
export XAUTHORITY=~/.Xauthority
export DISPLAY=:0.0

echo "Hello World"

if ps aux | grep -q "[g]nome-keyring-daemon "; then 
	echo "gnome-keyring-daemon found" 
else
	echo "Starting gnome-keyring-daemon"
	export $(gnome-keyring-daemon –-start)
fi

if ps aux | grep -q "[u]nclutter"; then 
	echo "mouse already hidden" 
else
	echo "Hiding mouse - unclutter"
	unclutter &
fi

midori -e Fullscreen -e Navigationbar -a https://status.lnls.br >>/dev/null & 