# raspi sec cam
- simple app that streams live and records while detecting human

## hardware
- raspberry pi 2/3/4
- raspbery pi camera module v1/2 or any usb camera
- sd card or usb boot

## installing
- use [rpi-imager](https://www.raspberrypi.com/software/) to create a usb or sd card boot
- install required libraries:
```sh
sudo apt update
sudo apt install -y python-opencv
sudo apt install -y python-pip
pip install -r requirements.txt
```

## usage
- modify desired args in src/constants.py
```sh
git clone https://github.com/uit-anhvuk13/pisecam.git
cd pisecam
python3 src/app.py
```
