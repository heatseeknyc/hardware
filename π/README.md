# Raspberry π


## Overview
- connect XBee to GPIO serial pins directly
- device is /dev/ttyAMA0
- then standard python `serial` library can be used


## Basic Setup
*get hub `<name>` from [the deployments spreadsheet](https://docs.google.com/spreadsheets/d/1yk-R_rF-0QqRmxfcSnsiBipPfZUVG2DtNUoTY1Ut6RI/edit)*
```sh
sudo raspi-config
# 1, 2, 4 > Locale, reboot
sudo raspi-config
# 4 > Change Timezone, 8 > Hostname > heatseek-hub-<name>, 8 > Serial > Off, reboot
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install emacs23-nox usb-modeswitch wvdial
sudo wvdialconf
sudo emacs /etc/wvdial.conf
# Phone = *99#
# Password = None
# Username = None
# Stupid Mode = 1
# Init3 = AT+CGDCONT=1,"IP","epc.tmobile.com"
# Auto DNS = off
sudo emacs /etc/ppp/peers/wvdial
# # usepeerdns
sudo emacs /etc/resolv.conf
# nameserver 8.8.8.8
# nameserver 8.8.4.4
sudo chattr +i /etc/resolv.conf
```


## Let the Internet In, Through an SSH Tunnel

### on the tunnel host (e.g. sparser.org)
```sh
sudo emacs /etc/ssh/sshd_config
# GatewayPorts yes
```

### on the π
*get port `<n>`umber from [the deployments spreadsheet](https://docs.google.com/spreadsheets/d/1yk-R_rF-0QqRmxfcSnsiBipPfZUVG2DtNUoTY1Ut6RI/edit)*
```sh
ssh-keygen
ssh-copy-id harold@sparser.org
crontab -e # get <n> from DEPLOYMENTS.md
# * * * * * ssh -fR '*:2200<n>:127.0.0.1:22' harold@sparser.org sleep 45 2>>cron-log.txt
# * * * * * curl -sSd "$(hostname)" http://requestb.in/13thhde1 2>>cron-log.txt
```


## (Optional) Direct Ethernet Connection to a Computer
**remove this when you're done, or things will misbehave**
```sh
emacs /Volumes/boot/cmdline.txt
# ip=169.254.169.254
```
