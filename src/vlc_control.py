from vlcclient import VLCClient
import config

vlc = VLCClient("::1")

vlc.connect()

vlc.clear()
vlc.enqueue(config.PLAYLIST_PATH)

# Play video1 looped
vlc.repeat_on()
vlc.play() 