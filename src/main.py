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
logging.basicConfig(level=config.LOG_LEVEL)
player = Player([config.VIDEO_PATH], config.VLC_ARGS)
player.set_loop()   # Important, don't delete!


def play_video1(*args):
    """ Play looped video1 """
    logging.info("play_video1")
    player.loop_fragment(*config.VIDEO1_POS)


def play_video2(*args):
    """ Play video2 then transition back to looped video1 """
    logging.info("play_video2")

    # If 2nd fragment is already playing, return
    if player.is_fragment_pos_set(*config.VIDEO2_POS):
        logging.info("Already playing video2, ignoring trigger")
        return

    player.play_fragment(*config.VIDEO2_POS, play_video1)


def schedule_video2(*args):
    """ On video1 end, transition to video2 """

    # If 2nd fragment is already playing, return
    if player.is_fragment_pos_set(*config.VIDEO2_POS):
        logging.info("Already playing video2, ignoring trigger")
        return

    logging.info("Scheduled transition to video2")

    video1_end_pos = config.VIDEO1_POS[1]
    player.register_on_position_callback(video1_end_pos, play_video2, *args)


# Init GPIO
if GPIO:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(config.TRIGGER_PIN, GPIO.FALLING, callback=schedule_video2, bouncetime=50)


def main():
    play_video1()

    while True:
        try:
            sleep(0.01)

        except KeyboardInterrupt:
            # schedule_video2()
            player.stop()
            return


if __name__ == '__main__':
    main()
