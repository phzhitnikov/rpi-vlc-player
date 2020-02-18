#!/bin/bash

AddToAutostart() {
	# Check if already added to autostart
	if ! grep -xqFe "$1" /etc/rc.local
	then
		sed -i -e '$i '"$1"'' /etc/rc.local
	fi
}

PLAYER_BASE_PATH="/home/pi/rpi-vlc-player"
PACKAGES="python3 python3-pip python3-venv python3-rpi.gpio vlc"
PYTHON_PACKAGES="python-vlc RPi.GPIO"

# Install dependencies
sudo apt update

echo "*** Installing packages: $PACKAGES"
sudo apt install $PACKAGES -y

echo "*** Creating python venv. This may take a while"
python3 -m venv env

echo "*** Installing python packages"
sudo env/bin/pip install $PYTHON_PACKAGES

echo "*** Adding start.sh script to autostart"
chmod +x start.sh
AddToAutostart ".$PLAYER_BASE_PATH/start.sh"
