#!/bin/bash

AddToAutostart() {
	# Check if already added to autostart
	if ! grep -xqFe "$1" /etc/rc.local
	then
		sed -i -e '$i '"$1"'' /etc/rc.local
	fi
}

PLAYER_BASE_PATH="/home/pi/rpi-vlc-player"

# Install dependencies
sudo apt update
sudo apt install python3 -y

pip3 install python-vlc

# Configure startup
AddToAutostart "$PLAYER_BASE_PATH/src/main.py &"
