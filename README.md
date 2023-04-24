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
sudo apt install -y python-pip
sudo apt install -y python-opencv
pip install flask
```

## usage
- modify desired args in src/constants.py
```sh
python3 src/app.js
```