VLC_ARGS = [
    "--no-osd",
    "--fullscreen",
    "--video-on-top",
    "--no-video-title-show",
    "--no-embedded-video",
    "--no-disable-screensaver",
    "--video-wallpaper"]

VIDEO_PATH = "../res/output.mp4"

# Video position for seeking (0-100)
# Try to avoid end_pos=100 due to freezing issues on loop restart
VIDEO1_POS = (0, 50)
VIDEO2_POS = (50, 95)

# Pins (BCM numeration!)
TRIGGER_PIN = 17
