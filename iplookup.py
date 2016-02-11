#!/usr/bin/env python2
#author: mp
#comment: scrape ipv4 information from whatismyipaddress.com
from BeautifulSoup import BeautifulSoup as Soup
import urllib2
import re
import sys

def usage():
    print "./iplookup.py <ipv4 address>"
    sys.exit()

try:
    ip = sys.argv[1]
except:
    usage()

if re.match( r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip ):
    opener = urllib2.build_opener()
    opener.addheaders = [( "User-agent", "Mozilla/5.0" )]                             
    data = Soup( opener.open( "http://whatismyipaddress.com/ip/{}".format( ip ) ).read() )
    for row in data.findAll( "tr" ):
        line = row.text #print pretty :)
        if "latitude" in line.lower() or "longitude" in line.lower():
            pass #i dont care for these results tbh
        elif "blacklist:" in line.lower():
            pass #scraping these results can be part of another script
        else:
            print line
else:
    print "!!! invalid ipv4 address"
    usage() #regex failed
