## Heat Seek NYC Hardware


### Overview

connect XBee to the π via serial GPIO pins

listen for IO frames, which are of the form 0x7E....92

use a (manually maintained) mapping of 64-bit sensor addresses to apartments, to record apartment temperatures


### XBee-DigiMesh

Unlike XBee Zigbee, it supports synchronized sleeping, for low-power meshing.

The [chip](http://www.digikey.com/product-detail/en/XB24-DMPIT-250/602-1338-ND/3482610) — this is the same hardware as [XBee Series 1](http://www.digikey.com/product-detail/en/XB24-API-001/602-1273-ND/3482588) but with DigiMesh firmware pre-installed.

The [docs](http://ftp1.digi.com/support/documentation/90000991_L.pdf).

Adding a new node is slightly trickier, but if the π node is in "Synchronous Sleep Support Mode" SM=7, then you can just bring a new node near the π at any time and it will sync up with the rest of the sleeping (SM=8) nodes.


### Alternatives

#### XBee-Zigbee

Can't both sleep and mesh, but has a better ADC, perhaps among other things.

Make sure to connect VREF to VCC. This is basically undocumented, but without it the chip basically crashes after a minute of reading from the ADC. _TODO_ email Digi about this.

The [chip](http://www.digikey.com/product-detail/en/XB24-Z7PIT-004/602-1275-ND/3482624), aka XBee Series 2.

The [docs](http://ftp1.digi.com/support/documentation/90000976_S.pdf)

### GERBER Files
If you need to generate a GERBER file, follow the instructions in [this tutorial](https://learn.sparkfun.com/tutorials/using-eagle-board-layout/generating-gerbers). You just clone [their repo](https://github.com/sparkfun/SparkFun_Eagle_Settings) and use `sfe-gerb274x.cam`.

