# Raspberry π


## Overview
- connect XBee to GPIO serial pins directly
- device is /dev/ttyAMA0
- then standard python `serial` library can be used


## Basic Setup
```sh
sudo raspi-config
# 1, 2, 4 > Locale, reboot
sudo raspi-config
# 4 > Change Timezone, Change Keyboard Layout, 8 > Serial > Off, reboot

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install usb-modeswitch wvdial supervisor python3-pip vnstat
sudo pip3 install -Ur requirements.txt

sudo ln -sf /home/pi/hardware/pi/conf/wvdial.conf /etc/
sudo emacs /etc/ppp/peers/wvdial
# # usepeerdns
sudo emacs /etc/resolv.conf
# nameserver 8.8.8.8
# nameserver 8.8.4.4
sudo chattr +i /etc/resolv.conf

sudo ssh-keygen
sudo ssh-copy-id hubs@hubs.heatseeknyc.com

sudo ln -s /home/pi/hardware/pi/conf/supervisor.conf /etc/supervisor/conf.d/heatseeknyc.conf
sudo supervisorctl reload
```


## (Optional) Direct Ethernet Connection to a Computer
**remove this when you're done, or things will misbehave**
```sh
emacs /Volumes/boot/cmdline.txt
# ip=169.254.169.254
```
