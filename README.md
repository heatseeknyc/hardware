## XBee notes


### coordinator node

**firmware** = ZigBee Coordinator API

**ID** = unique to this coordinator _i.e. unique to this building / sensor network_

**AR** = e.g. 6 _to set up "many-to-one" routes back to this coordinator every 6*10 seconds = 1 minute_


### sensor node

**firmware** = ZigBee Router AT

**PAN ID** = same as coordinator

(default) **DH/DL** = 0/0 _which sets the destination to be the coordinator_

(default) **AR** = 0xFF _which disables broadcasting routes to the sensor, because no one will ever be talking to the sensor_

**D1** = 2 _to set AD1 as analog read_

**IR** = e.g. 60000 _to sample every 60,000ms = 1 minute_

_TODO_ is it important to connect VREF to VCC?


## Raspberry π notes

### overview

connect to the coordinator node via usb board

listen for IO frames, which are of the form 0x7E....92

use a (manually maintained) mapping of 64-bit sensor addresses to apartments, to record apartment temperatures

### FTDI

FTDI's VCP drivers don't work on ARM (and thus π), so options are FTDI's D2XX, or the open source libftdi. We're going with libftdi.

pylibftdi doesn't support the new `0x6015` product ID, so our code adds it manually:

    pylibftdi.driver.USB_PID_LIST.append(0x6015)

_TODO_ look into why pylibftdi's read() method doesn't block as nicely as the builtin serial library
    
#### libftdi on Raspbian

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install libftdi-dev python3-setuptools
    sudo easy_install3 pip
    sudo pip3 install pylibftdi

and lastly, to allow FTDI devices to be opened without sudo:

    echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", GROUP="dialout", MODE="0660"' \
    | sudo tee /etc/udev/rules.d/99-libftdi.rules

#### libftdi on Mac OS X

    brew update
    brew upgrade
    brew install libftdi
    pip3 install pylibftdi

 If you have issues you may need to do:

    sudo kextunload -b com.apple.driver.AppleUSBFTDI

