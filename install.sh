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
sudo apt install vlc python3 -y

# Configure startup script
chmod +x "$PLAYER_BASE_PATH/start.sh"
AddToAutostart "$PLAYER_BASE_PATH/start.sh"