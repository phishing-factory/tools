#!/usr/bin/env python2

from BeautifulSoup import BeautifulSoup as Soup
import ssl
import urllib2
import sys

version = []
ssl._create_default_https_context = ssl._create_unverified_context
soup = Soup( urllib2.urlopen( "{}/docs/html/index.html".format( sys.argv[1] ) ).read() )
for div in soup.findAll( "div", { "class" : "related" } ):
    for ul in div.findAll( "ul" ):
        for a in div.findAll( "a" ):
            if "phpMyAdmin" in a.text:
                version.append( a.text.split( " " )[1] )
for i in version:
    print "[+] phpMyAdmin version {} detected".format( i )
    break
