printer-snmp-levels
===================

Get a printer consumable levels using SNMP

# Requirements

This utility requires Python 3 and EasySNMP. (python3-easysnmp on Debian-like, easysnmp-python on EL-like)

# Usage

```
usage: printer-snmp-levels.py [-h] host community

Get printer consumable levels using SNMP

positional arguments:
  host        The IP address or hostname of the printer
  community   The SNMP community to use (often 'public')
```

# Example

```
$ ./printer-snmp-levels.py 192.168.1.1 public
This is a HP LaserJet CM1415fn printer, named NPIAD0001 and with serial no. 1337DEADBF, up since the 2014-10-07

Consumable levels:
Black Cartridge HP CE320A has level 62%
Cyan Cartridge HP CE321A has level 63%
Magenta Cartridge HP CE323A has level 75%
Yellow Cartridge HP CE322A has level 63%

Please contact it@company.com for details.
```

# Supported printers

This utility has been tested with the following printer models:

* HP LaserJet CM1415fn
* Lexmark CX510de
* Xerox WorkCentre series

# Known issues

* Code lacks DRYness
