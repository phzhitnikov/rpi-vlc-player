import logging
import os
from time import sleep

import vlc

import config
from player import Player

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("No GPIO module. You're running on the rpi or not?")
    GPIO = None

os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.DEBUG)

player = Player([config.VIDEO_PATH], config.VLC_ARGS)


def play_video1(*args):
    logging.info("play_video1")
    player.loop_fragment(*config.VIDEO1_POS)


def play_video2(*args):
    logging.info("play_video2")

    # If 2nd fragment is already playing, return
    if player.is_fragment_pos_set(*config.VIDEO2_POS):
        logging.debug("Already playing video2, ignoring")
        return

    # Return to video1
    player.play_fragment(*config.VIDEO2_POS, play_video1)


# Init GPIO
if GPIO:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(config.TRIGGER_PIN, GPIO.FALLING, callback=play_video2, bouncetime=50)


def main():
    player.set_loop()   # Important!
    play_video1()

    while True:
        try:
            sleep(0.01)

        except KeyboardInterrupt:
            # play_video2()
            player.stop()
            return


if __name__ == '__main__':
    main()
