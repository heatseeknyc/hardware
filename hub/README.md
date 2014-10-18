## Hub node


### DigiMesh firmware

- **ID** = network id
- **NI** = "hub"
- **AP** = 1
- **SM** = 7
- **SO** = 1
- **SP** = 1770 (1 minute) or 57E40 (1 hour)


### Serial connection

- GPIO pin 1 (3v3) to XBee pin 1 (VCC)
- GPIO pin 6 (GND) to XBee pin 10 (GND)
- GPIO pin 8 (TXD) to XBee pin 3 (DIN)
- GPIO pin 10 (RXD) to XBee pin 2 (DOUT)

![GPIO pin layout](basic-gpio-layout.png)


### Data usage

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

Pre-paid Vodafone SIM cards:
- [1MB/month for a year](http://www.embeddedworks.net/wsim2730.html) for $31.27, or $2.61/MB
- [5MB/month for 6 months](http://www.embeddedworks.net/wsim2737.html) for $46.11, or $1.54/MB
- [10MB/month for a year](http://www.embeddedworks.net/wsim2786.html) for $137.41, or $1.15/MB


### 3G modems

There's a [generic stick](http://www.amazon.com/Generic-Wireless-7-2Mbps-Dongle-Function/dp/B00MHAKIJY/ref=sr_1_10?ie=UTF8&qid=1410451158&sr=8-10&keywords=usb+modem+wireless) for ~$13 and a [branded alternative](http://www.amazon.com/Huawei-E173-Unlocked-HSDPA-7-2Mbps/dp/B0055310KQ) for ~$26. Given that we currently budget $6 for a USB WiFi dongle, each of these represents some increase to the cost of the base, $7 and $20, respectively.

[Verified 3G USB dongles](http://elinux.org/RPi_VerifiedPeripherals#USB_3G_Dongles)


### Alternatives

connect the HSDPA (3G) dongle to an [Arduino USB Host Shield](https://www.sparkfun.com/products/9947), to see how easy direct USB 3G modem AT commands are... possibly not easy.

connect a [FONA GSM (2G) board](https://www.adafruit.com/fona) to an Arduino or whatever. this isn't cheaper than a Raspberry Pi, but could lead to a cheaper PCB.
