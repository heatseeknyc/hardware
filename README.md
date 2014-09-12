## demo notes

ssh into the Raspberry π and start the receiver and transmitter in a 'screen':

    cd heatseek
    screen -c screenrc
    
To switch between the tabs press Control-z then the tab number.

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

### new plan

connect XBee to GPIO serial pins directly

use the script at https://github.com/lurch/rpi-serial-console/ to enable serial

device is /dev/ttyAMA0

default π baud rate is 115200 but can be changed in the script, default XBee baud rate is 9600 but can be changed with the BD command, so whatever works best...

then standard python serial can be used, and no usb is used


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

#### Data usage notes

Assuming each reading is ~100 bytes (the reading itself may be as little as 20-30 bytes, plus the HTTP headers), and each cell takes 24 readings per day, that's 24 x 100 = 2,400 bytes per day per cell, or 2.4 kilobytes (roughly, 1kb = 1024b).

Assuming a base is connected to 10 cells, then the base will be transmitting 10 x 2.4 = 24 kilobytes per day.
Assuming 31 days per month (worst case), and 365 days per year, data usage will be:

|numCells|Data/Day|Data/Month|Data/120d|Data/Year|
|--------|--------|----------|---------|---------|
|1       |2.4 kb  |0.0744 mb |0.288 mb |0.876 mb |
|10      |24 kb   |0.744 mb  |2.88 mb  |8.76 mb  |
|15      |36 kb   |1.17 mb   |4.32 mb  |13.14 mb |
|20      |48 kb   |1.48 mb   |5.76 mb  |17.52 mb |
|30      |72 kb   |2.23 mb   |8.64 mb  |26.28 mb |
|50      |120 kb  |3.72 mb   |14.4 mb  |43.8 mb  |
|100     |240 kb  |7.44 mb   |28.8 mb  |87.6 mb  |

Researching data plans, the simplest plan was the [PagePlus](https://www.pagepluscellular.com/plans/10-standard-pin/) $10 prepaid. This plan offers data at $0.10 per megabyte, with a 120 day usage window per recharge. This means that every $10 recharge will allow us to transmit an additional 100 mb per base over a maximum of 120 days, far more than the needs of even our most ambitious deployments by nearly a factor of four. This means that we can reasonably expect data costs per base not to exceed $30/year under most circumstances.

Looking at this, then, it seems that we would be able to provide each base with more than sufficient data capacity for approximately $30/year for any size deployment. This is substantially cheaper than any other plans I was able to find, the next-cheapest of which cost approximately $10-20/month.

Regarding hardware, we would need to provide each base with a modem capable of translating between the Pi and the cellular network. Possibilities include this [generic stick](http://www.amazon.com/Generic-Wireless-7-2Mbps-Dongle-Function/dp/B00MHAKIJY/ref=sr_1_10?ie=UTF8&qid=1410451158&sr=8-10&keywords=usb+modem+wireless) for ~$13 and a [branded alternative](http://www.amazon.com/Huawei-E173-Unlocked-HSDPA-7-2Mbps/dp/B0055310KQ) for ~$26. Given that we currently budget $6 for a USB WiFi dongle, each of these represents some increase to the cost of the base, $7 and $20, respectively.

We need to consider whether the benefits of moving to cellular networks outweight the costs:

**PROS**
- Easier deployment (and re-deployment)
- More consistent deployment
- Remove dependence on building networks
- Remove the need to develop a wifi configuration process

**CONS**
- Additional base cost
- Annual data fee
- Larger size of base