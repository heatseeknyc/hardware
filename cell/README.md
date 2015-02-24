# Cell node


## Electrical

### Components

See the [spreadsheet](https://docs.google.com/spreadsheets/d/1aLX0yPriqRYv9exc7hV8ZaoWDZZKsPV997NUnLpyvPM/edit?usp=sharing).

#### Searching for capacitors
for now we're using Kemet X7R 50V ±10% ceramic 0805s and through-hole radial capacitors

so to search go [here](http://www.digikey.com/product-search/en?v=399&pv14=32&pv16=2&pv16=6&FV=fff40002%2Cfff8000b&stock=1&pbfree=1&rohs=1) and then filter by capacitance

### Power consumption

The input range of the MCP1700 is about 3.5V to absolute maximum 6.5V,
so we use 4xAAA batteries, which gives us an initial voltage of about 6.4V, and a voltage of about 4V after 1000mAh.

- MCP1700 quiescent current < 4µA
- XBee cyclic sleep current < 50µA
- Xbee transmit current < 45mA / 250mA PRO
- XBee idle/receive current < 50mA / 55mA PRO
- XBee ADC current **??**
- MCP9700 operating current < 12µA

**TODO** measure these!
- total sleeping current < 54µA
- total waking current < 50mA / 250mA PRO

#### Setup mode

If we transmit constantly, we use 50mA / 250mA PRO, so every hour of setup we use 1.3% / 6.3% PRO of the batteries.

#### Live mode

So if we transmit for 5 seconds every hour, we use 124µAh / 402µAh PRO per hour, so 4x1000mAh battery would last 3.6 / 1.1 PRO years.

And if we transmit for 10 seconds every hour, we use 193µAh / 749µAh PRO per hour, so 4x1000mAh battery would last 2.3 / 0.6 PRO years.


## Mechanical

### flat battery holder mounting

assuming symmetry, mounting hole centers are offset from left and right edges by (1.98" - 0.5") / 2 = 0.74"

terminals are offset from bottom by 0.102"

### XBee dimensions, including *full height* of [socket](http://www.sullinscorp.com/drawings/75_1BFC_10483.pdf)

XBee is smaller than XBee-PRO, `32.94mm - 5.33mm = 27.61mm`

    24.38mm W x 27.61mm D x 9.79mm (2.79mm + 7.0mm) H

### battery holder dimensions

[3d model](flat-case-squat-case-and-us-quarter.stl) of flat and squat cases and a quarter

#### [flat](http://www.digikey.com/product-detail/en/2481/2481K-ND/303826)

    50.79mm W x 54.51mm D x 23.29mm (13.5mm + 9.79mm) H
    2.00" W x 2.15" D x 0.92" H

#### [squat](http://www.digikey.com/product-detail/en/BH24AAAW/BH24AAAW-ND/38633)

    26mm W x 53mm D x 35mm (25mm + 10mm) H

### cases

#### [TS-3315P](http://www.polycase.com/ts-3315p)

    3.00" x 3.00" x 1.50", weight=2.1oz, volume=13.5""", price=$2.05

#### [LP-41P](http://www.polycase.com/lp-41p)

    3.29" x 3.29" x 1.25", weight=3.2oz, volume=13.53""", price=$2.66

#### [CU-791](http://www.budind.com/view/Plastic+Boxes/Utilibox+Style+E)

    3.08" x 3.08" x 1.50", weight=1.5oz, volume=14.23""", price=$2.86
