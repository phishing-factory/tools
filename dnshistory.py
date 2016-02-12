#!/usr/bin/env python2
#author: mp
#comment: scrape viewdns.info for a list of IPv4 addresses a domain has pointed to

from BeautifulSoup import BeautifulSoup as Soup
import urllib2
import sys

soup = Soup( urllib2.urlopen( "http://viewdns.info/iphistory/?domain={}".format( sys.argv[1] ) ).read() )
for table in soup.findAll( "table", { "border" : "1" } ):
    for tr in table.findAll( "tr" ):
        print tr.text
