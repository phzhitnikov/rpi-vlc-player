# Installation

1. Clone this repo to `/home/pi`:

```
cd /home/pi
git clone https://github.com/phzhitnikov/rpi-vlc-player.git
```

2. Run `INSTALL.sh`:

```
cd rpi-vlc-player
chmod +x INSTALL.sh
sudo ./INSTALL.sh
```

3. Copy your concatenated video to `res/` folder
4. Set `VIDEO_PATH` in `src/config.py`:

```
VIDEO_PATH = "res/output.mp4"
```

5. Configure seeking positions `VIDEO1_POS` & `VIDEO2_POS` (float value from 0 to 100) in `src/config.py`.

   Try to avoid end_pos=100 due to freezing issues on loop restart.

   Don't overlap video positions.

```
VIDEO1_POS = (0, 50)
VIDEO2_POS = (51, 95)
```

6. Configure `TRIGGER_PIN` in `src/config.py`. Attention: BCM numeration, more info: http://pinout.xyz

```
TRIGGER_PIN = 17
```

# Video creation

To concatenate multiple mp4 videos into one using `ffmpeg` tool:

1. Create `file_list.txt` in format `file <filename.mp4>`:

```
file video1.mp4
file video2.mp4
```

2. Run:

```
ffmpeg -f concat -i file_list.txt -c copy output.mp4
```

# Possible issues

- If video doesn't play on RPi due to `moov atom not found` error, repair your mp4 videos with [untrunc tool](https://github.com/ponchio/untrunc)
