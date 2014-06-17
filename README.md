## XBee notes

### coordinator node
firmware: ZigBee Coordinator API
PAN ID: unique to this coordinator (i.e. unique to this building / sensor network)
AR: e.g. 6, to set up "many-to-one" routes back to this coordinator every 6*10 seconds = 1 minute

### sensor node
firmware: ZigBee Router AT
PAN ID: same as coordinator
(default) DH/DL = 0/0, which sets the destination to be the coordinator
(default) AR = 0xFF, which disables broadcasting routes to the sensor, because no one will ever be talking to the sensor
D0 = 2, to set pin 0 as analog read
IR = e.g. 60,000, to sample every 60,000ms = 1 minute
