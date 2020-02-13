#!/bin/bash

PLAYER_BASE_PATH="/home/pi/rpi-vlc-player"

# Start vlc with telnet control
vlc --intf telnet --telnet-password admin --no-osd --fullscreen &

# Start main script
python3 $PLAYER_BASE_PATH/src/main.py &