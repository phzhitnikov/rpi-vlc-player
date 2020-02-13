# Installation
- Clone this repo to `/home/pi`:
```
cd /home/pi
git clone https://github.com/phzhitnikov/rpi-vlc-player.git
```
- Run `install.sh`:
```
chmod +x install.sh
./install.sh
```
- Copy your 2 video files to `res` folder
- Add relative video paths to `src/config.py`:
```
VIDEOS = ['res/video2.mov', 'res/video1.mov']
```
- Configure VIDEO2_DURATION in `src/config.py` 
```
VIDEO2_DURATION = 25.7
```
- Configure TRIGGER_PIN in `src/config.py`. Attention: BCM numeration, more info: http://pinout.xyz
```
TRIGGER_PIN = 17
```