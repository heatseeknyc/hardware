## demo notes

ssh into the Raspberry π and start the receiver and transmitter in a 'screen':

```bash
cd heatseek
screen
ruby transmit.rb
```

then press Control-z then press c, which creates a new tab, and run:

```bash
python3 -u receive.py >> data/readings.tsv
```

Now the transmitter and receiver are running, but we'll create one last tab for monitoring the output of the receiver.

Press Control-z then press c, to create another tab, then run:

```bash
tail -f data/readings.tsv
```
    
Now we have three tabs; to switch between them press Control-z then the tab number.

To 'detach' from the screen press Control-z then d.

To reattach to the screen, run `screen -r`.


## XBee-DigiMesh

Turns out we probably should have been using XBee DigiMesh instead of XBee Zigbee all along!

It supports synchronized sleeping, for low-power meshing.

The [chip](http://www.digikey.com/product-detail/en/XB24-DMPIT-250/602-1338-ND/3482610) — this is the same hardware as [XBee Series 1](http://www.digikey.com/product-detail/en/XB24-API-001/602-1273-ND/3482588) but with DigiMesh firmware pre-installed.

The [docs](http://ftp1.digi.com/support/documentation/90000991_L.pdf).

Adding a new node become slightly trickier, but if the π node is in "Synchronous Sleep Support Mode" SM=7, then you can just bring a new node near the π at any time and it will sync up with the rest of the sleeping (SM=8) nodes.

TODO - how to cause an I/O sample every time nodes wake up? Possibly large nonzero IR value will trigger just one initial read?

TODO - use EE=1 on all nodes, to enable encryption

### Power Consumption

cyclic sleep < 50µA

transmit < 45mA

So if we transmit for 1 second every hour, then we use 63µAh per hour, so a 1000mAh battery would last 1.8 years.

If we transmit for 5 seconds every hour, we use 112µAh per hour, so a 1000mAh battery would last 1.0 years.

If we transmit for 1 second every minute, we use 800µAh per hour, so a 1000mAh battery would last 52 days.

If we transmit for 5 seconds every minute, we use 3.8mAh per hour, so a 1000mAh battery would last 11 days.


## XBee-Zigbee

The [chip](http://www.digikey.com/product-detail/en/XB24-Z7PIT-004/602-1275-ND/3482624), aka XBee Series 2.

The [docs](http://ftp1.digi.com/support/documentation/90000976_S.pdf)

### coordinator node

**firmware** = ZigBee Coordinator API

**ID** = unique to this coordinator _i.e. unique to this building / sensor network_

**AR** = e.g. 6 _to set up "many-to-one" routes back to this coordinator every 6*10 seconds = 1 minute_


### sensor node

Connect VREF (pin 14) to VCC (aka 3.3V)! This is basically undocumented, but without it the chip basically crashes after a minute of reading from the ADC. _TODO_ email Digi about this.

**firmware** = ZigBee Router AT

**PAN ID** = same as coordinator

(default) **DH/DL** = 0/0 _which sets the destination to be the coordinator_

(default) **AR** = 0xFF _which disables broadcasting routes to the sensor, because no one will ever be talking to the sensor_

**D1** = 2 _to set AD1 as analog read_

**IR** = e.g. 60000 _to sample every 60,000ms = 1 minute_


## Raspberry π notes

### overview

connect to the coordinator node via usb board

listen for IO frames, which are of the form 0x7E....92

use a (manually maintained) mapping of 64-bit sensor addresses to apartments, to record apartment temperatures

### FTDI

FTDI's VCP drivers don't work on ARM (and thus π), so options are FTDI's D2XX, or the open source libftdi. We're going with libftdi.

pylibftdi doesn't support the new 0x6015 product ID, so our code adds it manually:

```python
pylibftdi.driver.USB_PID_LIST.append(0x6015)
```

pylibftdi's read() method doesn't block as nicely as the builtin serial library's read(), so we wrap it in a loop:

```python
def read(f, length):
    s = b''
    while True:
        s += f.read(length - len(s))
        if len(s) == length: break
        time.sleep(0.01)
    return s
```

    
#### libftdi on Raspbian

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install libftdi-dev python3-setuptools
sudo easy_install3 pip
sudo pip3 install pylibftdi
```

and lastly, to allow FTDI devices to be opened without sudo:

```bash
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", GROUP="dialout", MODE="0660"' \
| sudo tee /etc/udev/rules.d/99-libftdi.rules
```

#### libftdi on Mac OS X

```bash
brew update
brew upgrade
brew install libftdi
pip3 install pylibftdi
```

 If you have issues you may need to do:

```bash
sudo kextunload -b com.apple.driver.AppleUSBFTDI
```
