import logging

LOG_LEVEL = logging.INFO

VLC_ARGS = [
    "--no-osd",
    "--fullscreen",
    "--video-on-top",
    "--no-video-title-show",
    "--no-embedded-video",
    "--no-disable-screensaver",
    "--video-wallpaper"]

VIDEO_PATH = "../res/output.mp4"

# Video position for seeking (0.0 - 100.0)
# Try to avoid end_pos=100 due to freezing issues on loop restart
# Don't overlap video positions
VIDEO1_POS = (0, 50)
VIDEO2_POS = (51, 100)

# Pins (BCM numeration!)
TRIGGER_PIN = 17
