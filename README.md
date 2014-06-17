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

**D0** = 2 _to set pin 0 as analog read_

**IR** = e.g. 60000 _to sample every 60,000ms = 1 minute_


### raspberry π

listen for IO frames, which are of the form 0x7E....92

and then we'll need to (manually) maintain a mapping of 64-bit sensor addresses to apartments
