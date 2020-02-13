from time import sleep
from threading import Timer

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("No GPIO module. You're running on the rpi or not?")
    GPIO = None

import vlc
from vlc import PlaybackMode

import config

instance = vlc.Instance("--no-osd", "--fullscreen")
p = instance.media_list_player_new()
timer = Timer(config.VIDEO2_DURATION, None)


def play_video1():
    print("play_video1")

    p.play_item_at_index(0)
    p.set_playback_mode(PlaybackMode.repeat)


def play_video2():
    global timer

    # Ignore trigger if timer did not end
    if timer.is_alive():
        return

    print("play_video2")

    p.play_item_at_index(1)
    p.set_playback_mode(PlaybackMode.loop)

    timer = Timer(config.VIDEO2_DURATION, play_video1)
    timer.start()


# Init GPIO
if GPIO:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(config.TRIGGER_PIN, GPIO.FALLING, callback=play_video2, bouncetime=50)


def main():
    MediaList = instance.media_list_new(config.VIDEOS)
    p.set_media_list(MediaList)

    # Play video1 looped
    p.play_item_at_index(0)
    p.set_playback_mode(PlaybackMode.repeat)

    while True:
        try:
            sleep(0.01)

        except KeyboardInterrupt:
            p.stop()
            return


if __name__ == '__main__':
    main()
