if ps aux | grep -q "[g]nome-keyring-daemon "; then 
	echo "gnome-keyring-daemon found" 
	export $(gnome-keyring-daemon)
else
	echo "Starting gnome-keyring-daemon"
	export $(sudo gnome-keyring-daemon –-start)
fi

if ps aux | grep -q "[u]nclutter"; then 
	echo "mouse already hidden" 
else
	echo "Hiding mouse - unclutter"
	unclutter &
fi

export WEBKIT_IGNORE_SSL_ERRORS="1"
export XAUTHORITY=~/.Xauthority
export DISPLAY=:0.0

midori -e Fullscreen -e Navigationbar -a https://status.lnls.br >>/dev/null &
#firefox -url https://status.lnls.br/ -fullscreen &