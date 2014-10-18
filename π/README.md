## Raspberry π


### Overview

connect XBee to GPIO serial pins directly

device is /dev/ttyAMA0

then standard python `serial` library can be used


### Raspbian setup

    sudo raspi-config
    # 1, 2, 4 > Locale, then reboot
    # then the rest of 4, and 8 > Hostname and 8 > Serial > Off
    sudo apt-get update && sudo apt-get upgrade
    sudo apt-get install emacs23-nox screen usb-modeswitch wvdial
    sudo wvdialconf
    sudo emacs /etc/wvdial.conf
    # Phone = *99#
    # Password = None
    # Username = None
    # Stupid Mode = 1
    # Init3 = AT+CGDCONT=1,”IP”,”epc.tmobile.com”


### Demo notes

ssh into the Raspberry π and start the receiver and transmitter in a 'screen':

    cd hardware
    screen -c screenrc
    
To switch between the tabs press Control-z then the tab number.

To 'detach' from the screen press Control-z then d.

To reattach to the screen, run `screen -r`.
