#!/usr/bin/env python2
#author: mp
#comment: pull a list of IPv4 address for a given country

import urllib2
from BeautifulSoup import BeautifulSoup as Soup
import sys

soup = Soup( urllib2.urlopen( "http://www.nirsoft.net/countryip/" ).read() )
for i in soup.findAll( "a" ):
    if sys.argv[1] in i.text:
        csv = Soup( urllib2.urlopen( "http://www.nirsoft.net/countryip/{}.csv".format( i['href'].split( "." )[0] ) ) )

if csv:
    for line in csv:
        print line
