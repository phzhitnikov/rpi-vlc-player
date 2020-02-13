from time import sleep
from threading import Timer

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("No GPIO module. You're running on the rpi or not?")
    GPIO = None

from vlcclient import VLCClient
import config


vlc = VLCClient("::1")
timer = Timer(config.VIDEO2_DURATION, None)


def switch_back_video1():
    vlc.repeat_on()
    vlc.prev()


def trigger_video2():
    global timer

    # Ignore trigger if timer did not end
    if timer.is_alive():
        return

    vlc.repeat_off()
    vlc.next()

    # Set timer to switch back to video1 after VIDEO2_DURATION
    timer = Timer(config.VIDEO2_DURATION, switch_back_video1)
    timer.start()


# Init GPIO
if GPIO:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_callback(config.TRIGGER_PIN, trigger_video2)

def main():
    vlc.connect()

    vlc.clear()
    vlc.enqueue(config.PLAYLIST_PATH)

    # Play video1 looped
    vlc.repeat_on()
    vlc.play() 

    while True:
        try:
            sleep(0.01)

        except KeyboardInterrupt:
            # trigger_video2()
            vlc.stop()
            return
            


if __name__ == '__main__':
    main()