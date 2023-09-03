#!/usr/bin/python3
# Get SNMP-enabled printer consumables levels using SNMP

# Imports
import argparse
import re
import time
from datetime import date

from easysnmp import Session

# Functions
def getdetails(session):

  # HP ETHERNET MULTI-ENVIRONMENT,SN:XXXXXXXXXX,FN:XXXXXXX,SVCID:XXXXX,PID:HP LaserJet CM1415fn
  # Xerox WorkCentre 6505N; Net 95.45,ESS 201104251224,IOT 02.00.02,Boot 201009241127
  # Xerox WorkCentre 7845 v1; SS 072.040.004.09100, NC 072.044.09100, UI 072.044.09100, ME 090.079.000, CC 072.044.09100, DF 007.019.000, FI 032.054.000, FA 003.011.009, CCOS 072.004.09100, NCOS 072.004.09100, SC 008.088.000, SU 010.116.00294
  # Lexmark CX510de version NH63.GM.N638 kernel 3.0.0 All-N-1

  details = dict()

  # sysName.0
  details['name']    = session.get('.1.3.6.1.2.1.1.5.0').value

  # sysContact.0
  details['contact'] = session.get('.1.3.6.1.2.1.1.4.0').value

  # sysUpTimeInstance
  details['uptime'] = int(session.get('.1.3.6.1.2.1.1.3.0').value) / 100

  # sysDescr.0
  res = session.get('.1.3.6.1.2.1.1.1.0').value

  # Default details values (undefined values)
  details['pid']       = 'unknown'
  details['sn']        = 'unknown'

  if not details['contact']:
    details['contact'] = 'somebody'

  # Case 1: HP printer
  match = re.search(r'HP ETHERNET MULTI-ENVIRONMENT,SN:(.*),FN:(.*),SVCID:(.*),PID:(.*)', res)

  if match:

    details['pid']   = match.group(4)
    details['sn']    = match.group(1)

  # Case 2: Xerox printer
  match = re.search(r'Xerox (.*);', res)

  if match:

    details['pid']    = 'Xerox ' + match.group(1)
    details['sn']     = session.get('.1.3.6.1.2.1.43.5.1.1.17.1')

  # Case 3: Lexmark printer
  match = re.search(r'Lexmark (.*) version (.*) kernel (.*)', res)

  if match:

    # Lexmark CX510de XXXXXXXXXXXXX LW80.GM7.P210
    match          = re.search(r'(Lexmark .*) (.*) (.*)', session.get('.1.3.6.1.2.1.25.3.2.1.3.1').value)
    details['pid'] = match.group(1)
    details['sn']  = match.group(2)

  return details

def getconsumableslevels(session):

  consumables_number = len(session.walk('.1.3.6.1.2.1.43.11.1.1.6.1'))
  res = dict()

  for i in range(1, consumables_number + 1):

    res[i] = dict()

    res[i]['name'] = session.get(".1.3.6.1.2.1.43.11.1.1.6.1." + str(i)).value
    res[i]['level'] = session.get(".1.3.6.1.2.1.43.11.1.1.9.1." + str(i)).value

    # HACK: Some Lexmark printers may attempt to send back internationalized consumable names, try to workaround this by decoding the hex string
    # Why the heck does it use CP850 instead of ISO/UTF-8 ???
    if isinstance(res[i]['name'], bytes):
        res[i]['name'] = res[i]['name'].decode('cp850')

  return res

# Runtime
if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='Get printer consumables levels using SNMP')
  parser.add_argument('host', help="The IP address or hostname of the printer")
  parser.add_argument('community', help="The SNMP community to use (often 'public')")
  args = parser.parse_args()

  host = args.host
  community = args.community

  # Create an SNMP session to be used for all our requests
  session = Session(hostname=host, community=community, version=2)

  details = getdetails(session)

  print("This is a " + details['pid'] + " printer, named " + details['name'] + " and with serial no. " + details['sn'] + ", up since the " + str(date.fromtimestamp(time.time() - int(details['uptime']))) + "\n")

  levels = getconsumableslevels(session)

  print("Consumables levels (in % or remaining page number):")

  for key in levels:
    if levels[key]["name"]:
        print('* {:<60}: {}'.format(str(levels[key]["name"]), str(levels[key]["level"])))

  print("\nPlease contact " + details['contact'] + " for details.")
