#!/usr/bin/python
# -*- coding: utf8 -*-

# Get HP printer consumables levels using SNMP

# Imports
import argparse
import re
import netsnmp
import time
from datetime import date

# Functions
def getmib(mibentry):

  oid = netsnmp.Varbind(mibentry)
  res = netsnmp.snmpget(oid, Version = 1, DestHost=host, Community=community)
  return res[0]

def getdetails(host, community):

  # HP ETHERNET MULTI-ENVIRONMENT,SN:XXXXXXXXXX,FN:XXXXXXX,SVCID:XXXXX,PID:HP LaserJet CM1415fn
  # Xerox WorkCentre 6505N; Net 95.45,ESS 201104251224,IOT 02.00.02,Boot 201009241127
  # Xerox WorkCentre 7845 v1; SS 072.040.004.09100, NC 072.044.09100, UI 072.044.09100, ME 090.079.000, CC 072.044.09100, DF 007.019.000, FI 032.054.000, FA 003.011.009, CCOS 072.004.09100, NCOS 072.004.09100, SC 008.088.000, SU 010.116.00294

  details = dict()

  # sysName.0
  details['name']    = netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.2.1.1.5.0'), Version = 1, DestHost=host, Community=community)[0]

  # sysContact.0
  details['contact'] = netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.2.1.1.4.0'), Version = 1, DestHost=host, Community=community)[0]

  # sysUpTimeInstance
  details['uptime'] = int(netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.2.1.1.3.0'), Version = 1, DestHost=host, Community=community)[0]) / 100

  # sysDescr.0
  res = netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.2.1.1.1.0'), Version = 1, DestHost=host, Community=community)

  # Default details values (unknown)
  details['sn']    = 'unknown'
  details['fn']    = details['sn']
  details['svcid'] = details['sn']
  details['pid']   = details['sn']

  # Case 1: HP printer
  match = re.search(r'HP ETHERNET MULTI-ENVIRONMENT,SN:(.*),FN:(.*),SVCID:(.*),PID:(.*)', res[0])

  if match:

    details['sn']    = match.group(1)
    details['fn']    = match.group(2)
    details['svcid'] = match.group(3)
    details['pid']   = match.group(4)

  # Case 2: Xerox printer
  match = re.search(r'Xerox (.*);', res[0])

  if match:

    details['pid']    = 'Xerox ' + match.group(1)

  return details

def getconsumableslevels(host, community):

  consumables_number = len(netsnmp.snmpwalk(netsnmp.Varbind(".1.3.6.1.2.1.43.11.1.1.6.1"), Version = 1, DestHost=host, Community=community))
  res = dict()

  for i in range(1, consumables_number + 1):

    res[i] = dict()

    res[i]['name'] = netsnmp.snmpget(netsnmp.Varbind(".1.3.6.1.2.1.43.11.1.1.6.1." + str(i)), Version = 1, DestHost=host, Community=community)[0]
    res[i]['level'] = netsnmp.snmpget(netsnmp.Varbind(".1.3.6.1.2.1.43.11.1.1.9.1." + str(i)), Version = 1, DestHost=host, Community=community)[0]

  return res

# Runtime
if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='Get printer consumables levels using SNMP')
  parser.add_argument('host', help="The IP address or hostname of the printer")
  parser.add_argument('community', help="The SNMP community to use (often 'public')")
  args = parser.parse_args()

  host = args.host
  community = args.community

  details = getdetails(host, community)

  print "This is a " + details['pid'] + " printer, named " + details['name'] + " and with serial no. " + details['sn'] + ", up since the " + str(date.fromtimestamp(time.time() - int(details['uptime']))) + "\n"

  levels = getconsumableslevels(host, community)

  print "Consumables levels:"

  for key in levels:

    print "  * " + levels[key]["name"] + " level is " + levels[key]["level"] + " (% or pages left)"

  print "\nPlease contact " + details['contact'] + " for details."
