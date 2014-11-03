hp-snmp-levels
==============

Get HP printer cartridge levels using SNMP

# Requirements

This utility requires nothing that is not in python standard library.

It has been tested with 2.7.8.

# Usage

```
usage: hp-snmp-levels.py [-h] host community

Get HP printer cartridge levels using SNMP

positional arguments:
  host        The IP address or hostname of the printer
  community   The SNMP community to use (often 'public')
```

# Supported printers

This utility has been tested with the following printer models:

* HP LaserJet CM1415fn

# Known issues

* Will not autodetect the number of cartridges yet (assumes 4 for now)
* Code lacks DRYness
